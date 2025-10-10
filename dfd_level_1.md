```mermaid
graph TD
    subgraph DFD Level 1
        direction LR
        actor User

        subgraph KrushiAI System
            direction TB
            P1[1.0 Manage Web UI]
            P2[2.0 Analyze Plant Image]
            P3[3.0 Display Analytics]
            P4[4.0 Browse Disease Info]
        end

        DS1[(D1: ML Model)]
        DS2[(D2: Disease Info DB)]
        DS3[(D3: Training History)]

        User -- Plant Image --> P1
        User -- View Request --> P1
        P1 -- User Input --> P2
        P2 -- Prediction Request --> DS1
        DS1 -- Model Prediction --> P2
        P2 -- Disease Info Request --> DS2
        DS2 -- Disease Details --> P2
        P2 -- Analysis Result --> P1
        P1 -- Disease Diagnosis & Recommendations --> User

        User -- Analytics Request --> P1
        P1 -- Fetch Analytics --> P3
        P3 -- History Request --> DS3
        DS3 -- Training Stats --> P3
        P3 -- Performance Data --> P1
        P1 -- Analytics Dashboard --> User

        User -- Database Query --> P1
        P1 -- Fetch Disease Info --> P4
        P4 -- All Disease Data --> DS2
        DS2 -- Disease Records --> P4
        P4 -- Formatted Disease Info --> P1
        P1 -- Disease Database UI --> User
    end
```