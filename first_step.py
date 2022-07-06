import argparse
import json

from opentelemetry import trace, context
from opentelemetry.trace import NonRecordingSpan, SpanContext, TraceFlags
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, BatchSpanProcessor
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--context-file", help="temporary file holding job context")
    args = parser.parse_args()
    carrier = {}
    ctx = None
    if args.context_file:
        try:
            with open(args.context_file, 'r', encoding='utf-8') as f:
                carrier = json.load(f)
        except FileNotFoundError:
            with open(args.context_file, 'x', encoding='utf-8') as f:
                f.write("")
        except json.decoder.JSONDecodeError:
            pass

    trace.set_tracer_provider(TracerProvider())
    trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    tracer = trace.get_tracer(__name__)
    ctx = TraceContextTextMapPropagator().extract(carrier=carrier)
    context.attach(ctx)
    with tracer.start_as_current_span('first-trace'):
        TraceContextTextMapPropagator().inject(carrier)
        print("doing first things...")
    with open(args.context_file, 'w', encoding='utf-8') as f:
        f.write(json.dumps(carrier))


if __name__ == "__main__":
    main()
