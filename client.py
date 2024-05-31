import grpc
import templates_pb2
import templates_pb2_grpc
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

grpc_port = '127.0.0.1:50051'

def run():
    # Создаем канал для связи с сервером
    with grpc.insecure_channel(grpc_port) as channel:
        # Создаем клиента (stub)
        stub = templates_pb2_grpc.TemplatesStub(channel)

        # Тестирование CreateTemplate
        try:
            response = stub.CreateTemplate(templates_pb2.TemplateStruct(name="Test Template", description="A test template"))
            logger.info(f"CreateTemplate response: {response}")
        except grpc.RpcError as e:
            logger.error(f"CreateTemplate error: {e.details()}")

        # Тестирование UpdateTemplate
        try:
            stub.UpdateTemplate(templates_pb2.TemplateStruct(name="Updated Template", description="An updated template", id=response.id))
            logger.info(f"UpdateTemplate response: {response}")
        except grpc.RpcError as e:
            logger.error(f"UpdateTemplate error: {e.details()}")

        # Тестирование DeleteTemplate
        try:
            response = stub.DeleteTemplate(templates_pb2.IdStruct(id=response.id))
            logger.info(f"DeleteTemplate response: {response}")
        except grpc.RpcError as e:
            logger.error(f"DeleteTemplate error: {e.details()}")

        # Тестирование GetAllTemplates
        try:
            response = stub.GetAllTemplates(templates_pb2.Empty())
            logger.info(f"GetAllTemplates response: {response}")
        except grpc.RpcError as e:
            logger.error(f"GetAllTemplates error: {e.details()}")

        # Тестирование CreateLink
        try:
            response = stub.CreateLink(templates_pb2.FeatureLinkTemplateStruct(feature_id=1, template_id=1))
            logger.info(f"CreateLink response: {response}")
        except grpc.RpcError as e:
            logger.error(f"CreateLink error: {e.details()}")

        # Тестирование DeleteLink
        try:
            response = stub.DeleteLink(templates_pb2.FeatureLinkTemplateStruct(feature_id=1, template_id=1))
            logger.info(f"DeleteLink response: {response}")
        except grpc.RpcError as e:
            logger.error(f"DeleteLink error: {e.details()}")

        # Тестирование CreateFeature
        try:
            response = stub.CreateFeature(templates_pb2.FeatureStruct(name="New Feature"))
            logger.info(f"CreateFeature response: {response}")
        except grpc.RpcError as e:
            logger.error(f"CreateFeature error: {e.details()}")

        # Тестирование UpdateFeature
        try:
            response = stub.UpdateFeature(templates_pb2.FeatureStruct(id=1, name="Updated Feature"))
            logger.info(f"UpdateFeature response: {response}")
        except grpc.RpcError as e:
            logger.error(f"UpdateFeature error: {e.details()}")

        # Тестирование DeleteFeature
        try:
            response = stub.DeleteFeature(templates_pb2.IdStruct(id=1))
            logger.info(f"DeleteFeature response: {response}")
        except grpc.RpcError as e:
            logger.error(f"DeleteFeature error: {e.details()}")

        # Тестирование GetFeaturesByTemplateId
        try:
            response = stub.GetFeaturesByTemplateId(templates_pb2.IdStruct(id=1))
            logger.info(f"GetFeaturesByTemplateId response: {response}")
        except grpc.RpcError as e:
            logger.error(f"GetFeaturesByTemplateId error: {e.details()}")

if __name__ == "__main__":
    logger.info("Running gRPC client")
    run()
