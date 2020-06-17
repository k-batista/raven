# import logging

# from confluent_kafka import Consumer as KafkaConsumer
# from dynaconf import settings


# class LimitEventListener:
#     def __init__(self, app_context):
#         self.scheduler = app_context.scheduler
#         self.kafka_listener = KafkaConsumer({
#             'bootstrap.servers': settings.KAFKA.BROKERS,
#             'group.id': settings.KAFKA.GROUP_ID,
#             'auto.offset.reset': settings.KAFKA.RESET_POLICY
#         })
#         self.listener_timeout = settings.KAFKA.CONSUMER_TIMEOUT_SECONDS

#     def schedule(self):
#         self.kafka_listener.subscribe([settings.KAFKA.LIMIT_TOPIC])
#         self.scheduler.schedule_job(
#             self.__listen, interval=settings.KAFKA.POLLING_SECONDS)
#         logging.info(
#             f'Listening to Kafka -> '
#             f'topic={settings.KAFKA.LIMIT_TOPIC} '
#             f'brokers={settings.KAFKA.BROKERS} '
#             f'polling_interval={settings.KAFKA.POLLING_SECONDS}s '
#             f'consumer_timeout={settings.KAFKA.CONSUMER_TIMEOUT_SECONDS}ms')

#     def __listen(self):
#         event = self.kafka_listener.poll(self.listener_timeout)
#         logging.info(f'Received event from Kafka. customerId=')
