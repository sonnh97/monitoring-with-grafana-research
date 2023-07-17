from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
import subprocess

# Init tracer
resource = Resource(attributes={
    "service.name": "python-tracer/test"
})
trace.set_tracer_provider(TracerProvider(resource=resource,))
tracer = trace.get_tracer(__name__)

otlp_exporter = OTLPSpanExporter(endpoint="http://10.210.39.204:4317", insecure=True) # Grafana Agent grpc port
span_processor = BatchSpanProcessor(otlp_exporter)

trace.get_tracer_provider().add_span_processor(span_processor)


@tracer.start_as_current_span('root')
def aaa():
    trace.get_current_span().add_event('aaa')
    bbb()

    prop = TraceContextTextMapPropagator()
    carrier = {}
    prop.inject(carrier=carrier)
    subprocess.Popen(['/home/vinhlt/venv/bin/python3',
                      '/home/vinhlt/deploy/data_pipeline/test2.py', f"--traceid={carrier['traceparent']}"])
    import time
    time.sleep(10)
    ccc()
    ddd()


@tracer.start_as_current_span('bbb')
def bbb():
    trace.get_current_span().add_event('bbb')
    ddd()


@tracer.start_as_current_span('ccc')
def ccc():
    trace.get_current_span().add_event('ccc')


@tracer.start_as_current_span('ddd')
def ddd():
    trace.get_current_span().add_event('ddd')


if __name__ == '__main__':
    aaa()
