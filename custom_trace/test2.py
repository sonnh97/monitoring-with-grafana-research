import argparse
from opentelemetry.trace.propagation.tracecontext import     TraceContextTextMapPropagator
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor,  ConsoleSpanExporter

resource = Resource(attributes={
    "service.name": "python-tracer/test"
})

trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)

otlp_exporter = OTLPSpanExporter(endpoint="http://10.210.39.204:4317", insecure=True)

span_processor = BatchSpanProcessor(otlp_exporter)

trace.get_tracer_provider().add_span_processor(span_processor)

def eee(ctx):
    with tracer.start_as_current_span("eee", context=ctx) as span:
        trace.get_current_span().add_event('conchimcugay')
        trace.get_current_span().add_event('gay ooo')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Data loader')
    parser.add_argument('--traceid', type=str, nargs='?', default='', help='traceID')
    args = parser.parse_args()

    trace_id_str = args.traceid
    if trace_id_str is None or trace_id_str=='':
        raise ValueError
    carrier = {'traceparent': trace_id_str}

    trace.get_current_span().add_event(carrier)
    ctx = TraceContextTextMapPropagator().extract(carrier=carrier)
    eee(ctx)