# Battery CAN Protokolü Tanımı

Dosyadaki **CAN protokolü**, bir batarya yönetim sistemi (BMS) ile araç kontrol ünitesi (VCU) arasında gönderilen mesajların tanımını içeriyor. Kısaca özetleyeyim:

---

### 🔹 **Temel Yapı**

CAN protokolü, belirli mesaj ID’leri üzerinden periyodik olarak gönderilen verileri tanımlar. Her mesaj birden fazla sinyal (veri alanı) taşır.

| Alan               | Açıklama                                                              |
| ------------------ | --------------------------------------------------------------------- |
| **Msg Name**       | Mesajın adı (örneğin `PACK_STATUS`, `PACK_CURRENTS`, `PACK_VOLTAGES`) |
| **Msg ID**         | CAN hattında kullanılan kimlik numarası (örneğin `0x2`, `0x3`, `0x4`) |
| **Msg Cycle Time** | Mesajın gönderilme periyodu (örneğin 100 ms)                          |
| **Msg Length**     | Mesaj uzunluğu (örneğin 8 byte)                                       |
| **Signal Name**    | Mesaj içindeki tekil veri alanları                                    |
| **Byte Order**     | Veri sıralama tipi (`Intel` = little endian)                          |
| **Unit**           | Ölçü birimi (%, mA, mV vb.)                                           |

---

### 🔹 **Örnek Mesajlar**

#### 1. `PACK_STATUS` (ID: 0x2, 100 ms)

* **SOC (%):** State of Charge, bataryanın doluluk oranı
* **SOH (%):** State of Health, bataryanın sağlık durumu
* **Battery_States:** 0x0 = Standby, 0x1 = Precharge, 0x2 = Discharge, 0x3 = Charge

#### 2. `PACK_CURRENTS` (ID: 0x4, 100 ms)

* **Current (mA):** Anlık akım
* **Charging FET Status:** 0 = OFF, 1 = ON
* **Discharging FET Status:** 0 = OFF, 1 = ON

#### 3. `PACK_VOLTAGES` (ID: 0x3, 100 ms)

* **Min_Cell_Voltage (mV)**
* **Max_Cell_Voltage (mV)**
* **Cell_voltage_Delta:** Hücreler arası gerilim farkı

---

### 🔹 **Veri Akışı**

* Her mesaj **belirtilen periyotta (100 ms)** CAN hattına gönderilir.
* Her mesaj **8 byte** uzunluğundadır.
* Alıcı (örneğin VCU), mesaj ID’sine göre hangi datayı okuyacağını bilir.
* Gelen byte’lar tanımlı “Signal” alanlarına ayrıştırılarak anlamlı değerlere çevrilir (örneğin SOC = 75%).

---

### 🔹 **Özetle**

Bu protokolde:

* CAN hattında 0x2, 0x3, 0x4 gibi ID’lerle **batarya durumu, akımı ve voltajı** sürekli iletiliyor.
* Her mesaj **8 byte’lık veri** taşıyor.
* Bu veriler VCU veya izleme sistemi tarafından çözülerek bataryanın anlık durumu izleniyor.

---

### 🔹 **PACK_STATUS (Msg ID: 0x2)**

| Sinyal         | Başlangıç Bit | Uzunluk (bit) | Byte   | Açıklama                                                  | Birim |
| -------------- | ------------- | ------------- | ------ | --------------------------------------------------------- | ----- |
| SOC            | 0             | 8             | Byte 0 | Şarj durumu (0–100%)                                      | %     |
| SOH            | 8             | 8             | Byte 1 | Sağlık durumu (0–100%)                                    | %     |
| Battery_States | 16            | 8             | Byte 2 | 0x0: Standby, 0x1: Precharge, 0x2: Discharge, 0x3: Charge | -     |

---

### 🔹 **PACK_CURRENTS (Msg ID: 0x4)**

| Sinyal                 | Başlangıç Bit | Uzunluk (bit) | Byte          | Açıklama    | Birim |
| ---------------------- | ------------- | ------------- | ------------- | ----------- | ----- |
| Current                | 0             | 16            | Byte 0–1      | Akım değeri | mA    |
| Charging FET Status    | 16            | 1             | Byte 2, Bit 0 | 0=OFF, 1=ON | -     |
| Discharging FET Status | 17            | 1             | Byte 2, Bit 1 | 0=OFF, 1=ON | -     |

---

### 🔹 **PACK_VOLTAGES (Msg ID: 0x3)**

| Sinyal             | Başlangıç Bit | Uzunluk (bit) | Byte     | Açıklama                | Birim |
| ------------------ | ------------- | ------------- | -------- | ----------------------- | ----- |
| Min_Cell_Voltage   | 0             | 16            | Byte 0–1 | En düşük hücre voltajı  | mV    |
| Max_Cell_Voltage   | 16            | 16            | Byte 2–3 | En yüksek hücre voltajı | mV    |
| Cell_voltage_Delta | 32            | 16            | Byte 4–5 | Hücre farkı             | mV    |

---

Bu tabloya göre:

* Her mesaj **8 byte (64 bit)** uzunluğunda.
* Bit’ler **Intel (little-endian)** sıralamasıyla okunuyor.
* Her mesaj 100 ms’de bir CAN hattında tekrar gönderiliyor.

---

## 🔹 1. **PACK_STATUS (Msg ID: 0x2)**

**Tanım:**

* SOC (%)
* SOH (%)
* Battery_States

**CAN Frame (örnek):**

```
ID: 0x002
Data: 64 5F 02 00 00 00 00 00
```

**Açıklama:**

| Byte | Değer (Hex) | Anlamı                        |
| ---- | ----------- | ----------------------------- |
| 0    | 0x64        | **SOC = 100%**                |
| 1    | 0x5F        | **SOH = 95%**                 |
| 2    | 0x02        | **Battery State = Discharge** |
| 3–7  | 00          | Rezerve / kullanılmıyor       |

---

## 🔹 2. **PACK_CURRENTS (Msg ID: 0x4)**

**Tanım:**

* Current (mA)
* Charging FET Status
* Discharging FET Status

**CAN Frame (örnek):**

```
ID: 0x004
Data: 10 27 03 00 00 00 00 00
```

**Açıklama:**

| Byte | Değer (Hex) | Anlamı                                                          |
| ---- | ----------- | --------------------------------------------------------------- |
| 0–1  | 0x2710      | **Current = 10000 mA = 10 A**                                   |
| 2    | 0x03        | Bit 0 = 1 (**Charge FET ON**), Bit 1 = 1 (**Discharge FET ON**) |
| 3–7  | 00          | Boş                                                             |

---

## 🔹 3. **PACK_VOLTAGES (Msg ID: 0x3)**

**Tanım:**

* Min_Cell_Voltage (mV)
* Max_Cell_Voltage (mV)
* Cell_voltage_Delta (mV)

**CAN Frame (örnek):**

```
ID: 0x003
Data: 20 0F 24 0F 01 00 00 00
```

**Açıklama:**

| Byte | Değer (Hex) | Anlamı            |
| ---- | ----------- | ----------------- |
| 0–1  | 0x0F20      | **Min = 3872 mV** |
| 2–3  | 0x0F24      | **Max = 3876 mV** |
| 4–5  | 0x0001      | **Delta = 1 mV**  |
| 6–7  | 00          | Rezerve           |

---

## 🔹 Özetle:

| Mesaj         | ID  | Örnek Veri                | Anlam                              |
| ------------- | --- | ------------------------- | ---------------------------------- |
| PACK_STATUS   | 0x2 | `64 5F 02 00 00 00 00 00` | SOC=100%, SOH=95%, State=Discharge |
| PACK_CURRENTS | 0x4 | `10 27 03 00 00 00 00 00` | Current=10A, FETs=ON               |
| PACK_VOLTAGES | 0x3 | `20 0F 24 0F 01 00 00 00` | Min=3.872V, Max=3.876V             |
# veldocarbms