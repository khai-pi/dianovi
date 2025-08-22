### **Scenario**

You’re building a system that:

* Ingests **medical records** and **patient information** from a Hospital Information System (HIS).
* Runs **rule-based recommendations** (based on medical guidelines and billing rules) to optimize patient treatment.
* Provides a **UI for doctors** to view patient records and recommendations.
* Is **hosted in the cloud** (Azure suggested for familiarity, but any cloud is fine).

---

### **Deliverables**

#### **1. Architecture Overview**

Produce a **1–2 page architecture sketch** covering:

* Core services and API boundaries.
* Data stores and their purpose.
* Message flow and data lifecycle.
* Authentication & authorization model.
* Observability approach (logging, metrics, tracing).
* Reasoning for monolith vs. microservices.
* Scaling approach.

#### **2. Minimal Working Slice (Dockerized)**

Build a very small working prototype:

* **HIS Adapter** — reads a small sample JSON/CSV with patient data.
* **Recommendation Service** — returns dummy recommendations.
* **Doctor UI** — lists one patient and shows 1–2 recommendations.
* An **OpenAPI spec** for the API.

#### **3. DevOps / CI/CD Elements**

* **Dockerfiles** for each service.
* A **docker-compose** setup (or k3d/k8s manifests if you prefer).
* A simple **CI pipeline YAML** that:

  * Builds & lints code
  * Runs tests
  * Produces container images
* A short **CD plan** (no need to actually deploy).

#### **4. Security & Compliance Notes**

Briefly explain:

* How you would handle PHI securely (in transit & at rest).
* How secrets are managed.
* Access control for the UI.
