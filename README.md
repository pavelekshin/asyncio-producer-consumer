# Asyncio producer-consumer example with Queue and Event

```bash
.
├── README.md
├── .env
├── asyncio-endless-producer              - endless example of producer
│   ├── consumer.py
│   ├── main.py
│   ├── producer.py
│   └── resulthandler.py
├── asyncio-event-producer                - producer with Event
│   ├── consumer.py
│   ├── controller.py
│   ├── main.py
│   ├── producer.py
│   └── resulthandler.py
├── requrements.txt
├── ruff.toml
└── settings.py


```

### Requirements:
`cp .env.example .env`

### About:
- A complete examples showing how to implement a producer-consumer model using Python asyncio with Queue and Event.
- asyncio-event-producer - producer with event for kickoff worker tasks
- asyncio-endless-producer  - endless producer, program runtime 10s