import cv2
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from PIL import Image
import pytesseract

from util.db_operations import find_similar_card, find_similar_name
from util.phasher import phash_clip, image_height, image_width
from card import Base

DATABASE_URL = "postgresql://postgres:admin@localhost/cards_db"
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

engine = create_engine(DATABASE_URL, echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

cap = cv2.VideoCapture(1)

match_not_found = True
current_match = ""
current_entity_id = None
while match_not_found:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)  # Sort by area, largest first

    cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)

    approx_polys = [cv2.approxPolyDP(c, 0.04 * cv2.arcLength(c, True), True) for c in contours]

    approx_polys = [ap for ap in approx_polys if len(ap) == 4]

    bounding_boxes = sorted([cv2.boundingRect(ap) for ap in approx_polys], key=lambda bb: bb[2] * bb[3], reverse=True)

    largest_bb = bounding_boxes[0] if bounding_boxes else None

    if largest_bb:
        x, y, w, h = largest_bb
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    pil_image = None
    if len(largest_bb) > 0:
        x, y, w, h = largest_bb
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        clipped_image = frame[y:y + h, x:x + w]

        x_percent = int(round(h*0.05, 0))
        ten_percent = int(round(h*0.1, 0))
        eighty_percent = int(round(w*0.75, 0))
        roi_for_ocr = cv2.cvtColor(clipped_image[0:ten_percent, x_percent:eighty_percent], cv2.COLOR_BGR2GRAY)
        roi_thresh = cv2.threshold(roi_for_ocr, 150, 255, cv2.THRESH_BINARY_INV)[1]
        text = pytesseract.image_to_string(roi_thresh, config="--psm 7").strip("\n")

        ocr_result = None
        phash_result = None
        if len(text) > 3:
            ocr_result = find_similar_name(session, text)
            if ocr_result:
                cv2.putText(frame,
                            f"{ocr_result.name} {ocr_result.id}",
                            (x, y), cv2.FONT_HERSHEY_PLAIN,
                            2,
                            (0, 0, 0),
                            2, cv2.LINE_AA)
        else:
            cw, ch, _ = clipped_image.shape
            if cw > image_width * 0.8 or ch > image_height * 0.8:
                pil_image = (Image.fromarray(cv2.cvtColor(clipped_image, cv2.COLOR_BGR2RGB))
                             .resize((image_width, image_height)))
                perceptual_hash = phash_clip(pil_image)
                phash_result = find_similar_card(session, perceptual_hash)
                if phash_result is not None:
                    cv2.putText(frame,
                                f"{phash_result.name} {phash_result.id}",
                                (x, y), cv2.FONT_HERSHEY_PLAIN,
                                2,
                                (0, 0, 0),
                                2, cv2.LINE_AA)

    cv2.imshow("Original Webcam Feed", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
