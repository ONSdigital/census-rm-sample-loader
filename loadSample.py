import csv, pika, jinja2
import sys, getopt, uuid, os

# connect to rabbitmq server
# get rabbitmq env vars
rabbitmq_host       = os.environ.get('RABBITMQ_SERVICE_HOST', 'localhost')
rabbitmq_port       = os.environ.get('RABBITMQ_SERVICE_PORT', '5672')
rabbitmq_vhost      = os.environ.get('RABBITMQ_VHOST', '/')
rabbitmq_queue      = os.environ.get('RABBITMQ_QUEUE', 'localtest')
rabbitmq_exchange   = os.environ.get('RABBITMQ_EXCHANGE', '')
rabbitmq_user       = os.environ.get('RABBITMQ_USER', 'guest')
rabbitmq_password   = os.environ.get('RABBITMQ_PASSWORD', 'guest')

# set in init_rabbit
rabbitmq_credentials = None
rabbitmq_connection  = None
rabbitmq_channel     = None



# globally load sampleunit message template
env = jinja2.Environment(loader=jinja2.FileSystemLoader(["./"])) 
jinja_template = env.get_template( "message_template.xml") 



def sample_reader(file_obj,ce_uuid,ap_uuid,ci_uuid):
   
    reader = csv.DictReader(file_obj, delimiter=',')
    count = 0
    for sampleunit in reader:
        publish_sampleunit (jinja_template.render(sample=sampleunit, uuid=uuid.uuid4() , ce_uuid=ce_uuid ,ap_uuid=ap_uuid , ci_uuid=ci_uuid))
        count += 1
        if count % 5000 == 0:
            sys.stdout.write("\r" + str(count) + " samples loaded")
            sys.stdout.flush()
    
    print('\nAll Sample Units have been added to the queue ' +rabbitmq_queue )
    rabbitmq_connection.close()

        

def publish_sampleunit(message):
   
    rabbitmq_channel.basic_publish(exchange=rabbitmq_exchange,
                      routing_key=rabbitmq_queue,
                      body=str(message),
                      properties=pika.BasicProperties(content_type='text/xml')
                    )

def init_rabbit():
    global rabbitmq_credentials, rabbitmq_connection, rabbitmq_channel 
    rabbitmq_credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
    rabbitmq_connection = pika.BlockingConnection(
                        pika.ConnectionParameters(rabbitmq_host,
                                                  rabbitmq_port,
                                                  rabbitmq_vhost,
                                                  rabbitmq_credentials))
    rabbitmq_channel = rabbitmq_connection.channel()

    if rabbitmq_queue == 'localtest':
        rabbitmq_channel.queue_declare(queue=rabbitmq_queue)

#----------------------------------------------------------------------
# Usage python loadSample.py <SAMPLE.csv> <COLLECTION_EXERCISE_UUID> <ACTIONPLAN_UUID> <COLLECTION_INSTRUMENT_UUID>
# 
def main(argv):  
    if len(sys.argv) < 4:
      print('Usage python loadSample.py sample.csv <COLLECTION_EXERCISE_UUID> <ACTIONPLAN_UUID> <COLLECTION_INSTRUMENT_UUID>')
    else:
      init_rabbit()
      with open(sys.argv[1]) as f_obj:
         sample_reader(f_obj,sys.argv[2],sys.argv[3],sys.argv[4]) 

if __name__ == "__main__":
    main(sys.argv)