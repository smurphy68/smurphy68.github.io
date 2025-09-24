package services

import (
	"strconv"

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
	conn, e := kafka.Dial("tcp", broker)
	checkError(e)

	controller, e := conn.Controller()
	checkError(e)

	var controllerConn *kafka.Conn
	controllerConn, e = kafka.Dial("tcp", controller.Host+":"+strconv.Itoa(controller.Port))
	checkError(e)

	topicConfigs := []kafka.TopicConfig{
		{
			Topic:             topic,
			NumPartitions:     1,
			ReplicationFactor: 1,
		},
	}

	e = controllerConn.CreateTopics(topicConfigs...)
	checkError(e)

	defer conn.Close()
}

func checkError(e error) bool {
	if e != nil {
		errorService.HandleError(e)
		return true
	}
	return false
}
