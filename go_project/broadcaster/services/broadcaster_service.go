package services

import (
	"fmt"
	"log"
	"time"

	"github.com/segmentio/kafka-go"
	errorService "github.com/smurphy68/go_project/shared/shared_services"
)

func Writer(brokers []string, topic string) *kafka.Writer {
	var writerConfig = kafka.WriterConfig{
		Brokers: brokers,
		Topic:   topic,
	}
	return kafka.NewWriter(writerConfig)
}

func TryStartTopic(broker, topic string) {
	var conn *kafka.Conn
	var e error

	// TODO: Is this bad?
	for {
		conn, e = kafka.Dial("tcp", broker)
		if e != nil {
			errorService.HandleError(e, "INFO")
			time.Sleep(time.Second * 5)
			continue
		} else {
			defer conn.Close()
			controller, e := conn.Controller()
			if e != nil {
				errorService.HandleError(e, "INFO")
				return
			}
			controllerAddr := fmt.Sprintf("%s:%d", controller.Host, controller.Port)
			controllerConn, e := kafka.Dial("tcp", controllerAddr)
			if e != nil {
				errorService.HandleError(e, "INFO")
				return
			}
			defer controllerConn.Close()

			topicConfigs := []kafka.TopicConfig{
				{
					Topic:             topic,
					NumPartitions:     1,
					ReplicationFactor: 1,
				},
			}

			if err := controllerConn.CreateTopics(topicConfigs...); err != nil {
				log.Fatalf("Failed to create Kafka topic: %v", err)
			}

			log.Printf("✅ Topic '%s' created or already exists", topic)
			break
		}
	}
}
