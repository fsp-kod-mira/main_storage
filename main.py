import grpc
import templates_pb2
import templates_pb2_grpc
from grpc_reflection.v1alpha import reflection
from concurrent import futures
import logging
import model
import os


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

grpc_port = os.environ.get('GRPC_IPPORT') or '0.0.0.0:50051'



def print_exception_details(e, context):
    logger.error(f"Error: {e}")
    logger.exception(e)
    context.set_code(grpc.StatusCode.INTERNAL)
    context.set_details(str(e))



class TemplatesServicer(templates_pb2_grpc.TemplatesServicer):
    


#========================================================================================================================
#                   Templates
#========================================================================================================================



    def CreateTemplate(self, request, context):
        """
        Добавление шаблона
        """
        logger.info("CreateTemplate request")
        try:
            id = model.CreateTemplate(request.name, request.description)
            return templates_pb2.IdStruct(id=id)
        except Exception as e:
            print_exception_details(e, context)
            return templates_pb2.IdStruct()



    def UpdateTemplate(self, request, context):
        """
        Обновление шаблонов
        """
        logger.info("UpdateTemplate request")
        try:
            model.UpdateTemplate(request.name, request.description, request.id)
        except Exception as e:
            print_exception_details(e, context)
        return templates_pb2.Empty()



    def DeleteTemplate(self, request, context):
        """
        Удалить шаблон
        """
        logger.info("DeleteTemplate request")
        try:
            model.DeleteTemplate(request.id)
        except Exception as e:
            print_exception_details(e, context)        
        return templates_pb2.Empty()



#========================================================================================================================
#              Links
#========================================================================================================================



    def CreateLink(self, request, context):
        """
        Создание связи между таблицами
        """
        logger.info("CreateLink request")
        try:
            id = model.AddTemplateFeatureLink(request.feature_id, request.template_id, request.value)
            return templates_pb2.IdStruct(id=id)
        except Exception as e:
            print_exception_details(e, context)

        return templates_pb2.IdStruct(id=-1)



    def UpdateLink(self, request, context):
        """
        Редактирование связи
        """
        logger.info("UpdateLink request")
        try:
            model.UpdateTemplateFeaturesLink(request.feature_id, request.template_id, request.value)
        except Exception as e:
            print_exception_details(e, context)

        return templates_pb2.Empty()


    
    def DeleteLink(self, request, context):
        """
        Удалить связь между таблицами
        """
        logger.info("DeleteLink request")
        try:
            
            model.DeleteTemplateFeatureLink(request.feature_id, request.template_id)
        except Exception as e:
            print_exception_details(e, context)
        
        return templates_pb2.Empty()



#========================================================================================================================
#                       Feature
#========================================================================================================================



    def CreateFeature(self, request, context):
        """
        Создание фичи
        """
        logger.info("CreateFeature request")

        try:
            id = model.CreateFeature(request.name, request.feature_type)
            return templates_pb2.IdStruct(id=id)
        except Exception as e:
            print_exception_details(e, context)
        
        return templates_pb2.Empty()    


    
    def UpdateFeature(self, request, context):
        """
        Обновление фичи
        """
        logger.info("UpdateFeature")

        try:
            model.UpdateFeature(request.id, request.name, request.feature_type)
        except Exception as e:
            print_exception_details(e, context)

        return templates_pb2.Empty()



    def DeleteFeature(self, request, context):
        """
        Удаление фичи
        """
        logger.info("DeleteFeature")
        try:
            model.DeleteFeature(request.id)
        except Exception as e:
            print_exception_details(e, context)

        return templates_pb2.Empty()



#========================================================================================================================
#                       MORE MORE MORE DATA!!!
#========================================================================================================================


    """
                    deprecated
    def fGetFeaturesByTemplateId(self, request, context):
        
        Получение фич по айди шаблона
        
        logger.info("GetFeaturesByTemplateId request")
        try:
            ret_features = templates_pb2.FeaturesList()
            templates_result = model.GetFeaturesByTemplateId(request.id)
            for feature in templates_result:
                temp_struct = templates_pb2.FeatureStruct(id=feature["id"], name=feature["name"])
                ret_features.items.append(temp_struct)
            return ret_features
        except Exception as e:
            print_exception_details(e, context)
        return templates_pb2.FeaturesList()
    """ 



    def GetFeaturesByTemplateId(self, request, context):
        """
        Получение фич по айди шаблона
        """
        logger.info("GetFeaturesByTemplateId request")
        try:
            final_array = templates_pb2.HibridFeatureLinkTemplateList()
            database_result = model.GetFeaturesByTemplateId(request.id)

            for row in database_result:
                """
                uint64 id = 1;
                uint64 feature_id = 2;
                uint64 template_id = 3;
                string value = 4;

                {'id': 1, 'name': 'tempor aliquip', 'feature_type': 0, 
                'link': {'id': 1, 'feature_id': 1, 'template_id': 1, 
                'value': 'какое то значение в валуе'}}

                
                "id": feature.id,
                    "name": feature.name,
                    "feature_type": feature.feature_type,
                    "link":{
                        "id": link.id,
                        "feature_id": link.feature_id, 
                        "template_id": link.template_id,
                        "value": link.value
                    }

                """
                temp_link = templates_pb2.FeatureLinkTemplateStruct(
                        id=row["link"]["id"],
                        feature_id=row["link"]["feature_id"],
                        template_id=row["link"]["template_id"],
                        value=row["link"]["value"]
                    )
                """
                uint64 id = 1;
                string name = 2;
                FeatureType feature_type = 3;
                """
                temp_feature = templates_pb2.FeatureStruct(
                        id=row["id"],
                        feature_type=row["feature_type"],
                        name=row["name"],
                    )
                item = templates_pb2.FeatureLinkTemplate(link=temp_link, feature=temp_feature)
                final_array.items.append(item)

            return final_array
        except Exception as e:
            print_exception_details(e, context)
        return templates_pb2.HibridFeatureLinkTemplateList()
    



    def GetAllTemplates(self, request, context):
        """
        Получение всех шаблонов
        """
        logger.info("GetAllTemplates request")
        try:
            ret_templates = templates_pb2.TemplatesList()
            templates_result = model.GetAllTemplates()

            for template in templates_result:
                temp_struct = templates_pb2.TemplateStruct(
                    id=template["id"],
                    name = template["name"], 
                    description = template["description"])
                ret_templates.items.append(temp_struct)
            return ret_templates
        
        except Exception as e:
            print_exception_details(e, context)
        
        return templates_pb2.TemplatesList()    


    









def serve():
    try:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        templates_pb2_grpc.add_TemplatesServicer_to_server(TemplatesServicer(), server)
        SERVICE_NAMES = (
            templates_pb2.DESCRIPTOR.services_by_name['Templates'].full_name,
            reflection.SERVICE_NAME,
        )

        reflection.enable_server_reflection(SERVICE_NAMES, server)
        server.add_insecure_port(grpc_port)
        server.start()
        server.wait_for_termination()
    except Exception as e:
        logger.error("Error in server:", e)


if __name__ == "__main__":
    logger.info(f"Run server on {grpc_port}")
    serve()
