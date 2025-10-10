```mermaid
graph TD
    subgraph DFD Level 0 - Context Diagram
        direction LR
        actor User
        rectangle KrushiAI_System[KrushiAI System]

        User -- Plant Image --> KrushiAI_System
        KrushiAI_System -- Disease Diagnosis & Recommendations --> User
    end
```