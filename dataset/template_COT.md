---
system: You are a procedural assistant trained to guide users through technical SOPs step-by-step with clarity and reasoning.
user: Start SOP: Template Light AR for Line Operators (Doc ID: WI-320)
---

**Assistant:**

Understood. This SOP covers the procedure to connect the HD module to the Adapter and the Board using Raspberry Pi 4B.  
There are 4 main steps in the procedure. Let me guide you through them.

**Reasoning:** Before starting, it's important to understand the end-to-end flow. The SOP is broken down into steps that ensure the hardware is correctly connected and verified using system tools.

---

---
system: You are a procedural assistant trained to guide users through technical SOPs step-by-step with clarity and reasoning.
user: What tools or parts do I need to complete this SOP?
---

**Assistant:**

You’ll need the following components:  
- PN001: Raspberry Pi PoE  
- PN002: Module 4 IO Board  
- PN023: IMX477 Sensor Block  
- PN029: DSI display FPC connectors (22-pin 0.5 mm pitch cable)  
- PN030: Module 4 Antenna Kit

**Reasoning:** These parts form the necessary assembly for capturing and transmitting high-resolution video from the HD module to the Raspberry Pi board. Without these, the SOP cannot be completed.

---

---
system: You are a procedural assistant trained to guide users through technical SOPs step-by-step with clarity and reasoning.
user: What is Step 1 of the procedure?
---

**Assistant:**

Step 1: Connect the HD module to the Adapter.  
- Insert the FPC cable from the HD module into the connector on the Adapter.  
- Secure the FPC cable in place by tightening the screws on the connector.

**Reasoning:** The HD module outputs data via a flexible FPC cable. Connecting it securely to the Adapter is critical, as this adapter translates the camera's output into USB-compatible signals.

---

---
system: You are a procedural assistant trained to guide users through technical SOPs step-by-step with clarity and reasoning.
user: I've finished Step 1. What's next?
---

**Assistant:**

Step 2: Connect the Adapter to the Board.  
- Insert the USB connector on the Adapter into any available USB port on the Board.  
- Ensure that the Adapter is securely attached to the Board.

**Reasoning:** Now that the Adapter carries the camera signal, it must relay that signal to the Raspberry Pi board via USB. A loose connection here would prevent device recognition.

---

---
system: You are a procedural assistant trained to guide users through technical SOPs step-by-step with clarity and reasoning.
user: How do I power it on after connecting everything?
---

**Assistant:**

Step 3: Power on the Board.  
- Connect the power supply to the Board.  
- Power on the Board by pressing the power button or connecting the power supply.

**Reasoning:** Without power, the Raspberry Pi won't initialize its USB interface, meaning the adapter and camera will remain unrecognized. Power-up enables the system to begin device enumeration.

---

---
system: You are a procedural assistant trained to guide users through technical SOPs step-by-step with clarity and reasoning.
user: How do I know if the adapter is working?
---

**Assistant:**

Step 4: Verify the Connection.  
- Open a terminal window on the Board.  
- Type `lsusb`.  
- Verify that the Adapter appears as a connected USB device.

**Reasoning:** The `lsusb` command lists all detected USB devices. If the Adapter appears here, it confirms that the physical connection and power delivery were successful.

---

---
system: You are a procedural assistant trained to guide users through technical SOPs step-by-step with clarity and reasoning.
user: What does FPC cable mean?
---

**Assistant:**

FPC cable stands for Flexible Printed Circuit cable.  
It's a ribbon-style cable commonly used to connect components in compact electronics.

**Reasoning:** FPC cables are preferred in embedded systems because of their flexibility and compact form factor. They're ideal for camera-to-adapter connections where space is limited.

---
