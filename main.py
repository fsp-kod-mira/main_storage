import grpc
import templates_pb2
import templates_pb2_grpc
from grpc_reflection.v1alpha import reflection
from concurrent import futures
import model


grpc_port = '[::]:50051'

class TemplatesServicer(templates_pb2_grpc.TemplatesServicer):
    
    def CreateTemplate(self, request, context):
        try:
            id = model.AddTemplate(request.name, request.description)
            return templates_pb2.IdStruct(id=id)
        except Exception as e:
            print("Error in CreateTemplate:", e)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return templates_pb2.IdStruct()


    def CreateLink(self, request, context):
        try:
            id = model.AddFeatureTemplateLink(request.feature_id, request.template_id)
            return templates_pb2.IdStruct(id=id)
        except Exception as e:
            print("Error in CreateLink:", e)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return templates_pb2.IdStruct()



    def GetAllTemplates(self, request, context):
        try:
            ret_templates = templates_pb2.TemplatesList()
            templates_result = model.GetAllTemplates()

            for template in templates_result:
                temp_struct = templates_pb2.TemplateStruct(id=template["id"], name=template["name"], description=template["description"])
                ret_templates.items.append(temp_struct)

            return ret_templates
        except Exception as e:
            print("Error in GetAllTemplates:", e)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return templates_pb2.TemplatesList()
            

    
    def GetFeaturesByTemplateId(self, request, context):
        try:
            ret_features = templates_pb2.FeaturesList()
            templates_result = model.GetFeaturesByTemplateId(request.id)
            print(templates_result)

            for feature in templates_result:
                print(feature)

                temp_struct = templates_pb2.FeatureStruct(id=feature["id"], name=feature["name"], priority_id=feature["priority_id"])
                print("add")
                ret_features.items.append(temp_struct)

            return ret_features
        except Exception as e:
            print("Error in GetFeaturesByTemplateId:", e)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return templates_pb2.FeaturesList()
        









    def DeleteLink(self, request, context):
        try:
            print(request.feature_id)
            model.DeleteFeatureTemplateLink(request.feature_id, request.template_id)
        except Exception as e:
            print("Error in DeleteLink:", e)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
        
        return templates_pb2.Empty()



    def DeleteTemplate(self, request, context):
        try:
            model.DeleteTemplate(request.id)
        except Exception as e:
            print("Error in DeleteTemplate:", e)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
        
        return templates_pb2.Empty()








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
        print("Error in server:", e)

if __name__ == "__main__":
    print(f"Run server on {grpc_port}")
    serve()
