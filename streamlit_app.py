import streamlit as st
import pandas as pd
from datetime import datetime, date
import os

# File path for local storage
excel_file = ""

# Helper function to calculate time in months
def calculate_months(start_date, end_date):
    return (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)

# Load existing data or create a new DataFrame
def load_data():
    if os.path.exists(excel_file):
        return pd.read_excel(excel_file)
    else:
        return pd.DataFrame(columns=[
            "MRN", "Date_of_Birth", "Age", "Date_of_Last_Radiotherapy", "Follow_up_date", "Follow_up_time",
            "Histology", "Grade", "Tumor_Focality", "Clinical_Stage", "Type_of_Confirmatory_procedure", "Biopsy_date",
            "Recurrent_Tumor", "Recurrence_date", "Surgery_type", "Surgery_date", "Systemic_Treatment", "Systemic_Treatment_first_date", "Systemic_Treatment_last_date",
            "Dose", "Fractionation", "Dysuria", "Cystitis", "Bladder_Perforation", "Hematuria", "Urinary_Fistula", "Urinary_Obstruction", "Ureteral_Stenosis", "Diarrhea", "Nausea", "Bowel_Perforation", "Bowel_Obstruction", "Fatigue", "Overal_tolerance",
            "Local_recurrence", "Regional_recurrence", "Distant_recurrence", "Death", "time_to_local_recurrence", "time_to_regional_recurrence", "time_to_distant_recurrence", "time_to_death"
        ])

# Function to safely retrieve data, handling NaN values
def safe_get(data, key, default=""):
    value = data.get(key, default)
    return value if pd.notna(value) else default

# Function to safely retrieve a list from stored string values
def safe_get_list(data, key):
    value = data.get(key, "")
    if pd.isna(value) or not isinstance(value, str):
        return []
    return [item.strip() for item in value.replace("[", "").replace("]", "").replace("'", "").split(",") if item]


# Function to fetch existing patient data by MRN
def get_patient_data(mrn):
    df = load_data()
    df["MRN"] = df["MRN"].astype(str).str.strip()
    mrn = str(mrn).strip()
    if mrn in df["MRN"].values:
        return df[df["MRN"] == mrn].iloc[0].to_dict()
    return None

# Function to save patient data (Appending Instead of Overwriting)
def save_data(data):
    df = load_data()
    df["MRN"] = df["MRN"].astype(str).str.strip()
    data["MRN"] = str(data["MRN"]).strip()

    # Append new data as a separate row instead of replacing the existing one
    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)

    # Save the updated DataFrame
    df.to_excel(excel_file, index=False)


# Streamlit app layout
st.title("Patient Information Database - Renal and Upper Tract Cancer Prospective Registry")

# Input for MRN
mrn = st.text_input("Enter MRN (Medical Record Number) and press Enter", key="mrn")

# Fetch existing patient data
patient_data = get_patient_data(mrn) if mrn else None

# Start the form
with st.form("patient_form", clear_on_submit=False):
    st.subheader("Patient Details")

    date_of_birth = st.date_input("Date of Birth",
        value=datetime.strptime(safe_get(patient_data, "Date_of_Birth", "1900-01-01"), "%Y-%m-%d").date() if patient_data else date.today(), min_value=datetime(1900, 1, 1).date(), max_value=datetime.today().date()
    )

    mrn = st.text_input("MRN (Medical Record Number)", value=mrn)

    last_radiotherapy_date = st.date_input("Date of Last Radiotherapy",
        value=datetime.strptime(safe_get(patient_data, "Date_of_Last_Radiotherapy", "1900-01-01"), "%Y-%m-%d").date() if patient_data else date.today()
    )

    follow_up_date = st.date_input("Date of Follow-up",
        value=datetime.strptime(safe_get(patient_data, "Follow_up_date", "1900-01-01"), "%Y-%m-%d").date() if patient_data else date.today()
    )

    Histology = st.multiselect("Histology", ["Renal Cell Carcinoma", "Papilary Renal Cell Tumors", "Oncocytic and chromophobe renal tumors", "Renal mesenchymal tumors", "Other renal tumors"],
       default=safe_get_list(patient_data, "Histology") if patient_data else []
    )
    st.warning("Not sure about histological classification? Click [here](https://www.pathologyoutlines.com/topic/kidneytumorWHOclass.html) to use Pathology Outlines.")

    Grade = st.radio("Grade", ["I", "II", "III", "IV", "Not Reported"],
        index=["I", "II", "III", "IV", "Not Reported"].index(safe_get(patient_data, "Grade", "Not Reported")) if patient_data else 0
    )

    Tumor_Focality = st.radio("Tumor_Focality", ["Unifocal", "Multifocal", "Not Reported"],
        index=["Unifocal", "Multifocal", "Not Reported"].index(safe_get(patient_data, "Tumor_Focality", "Unifocal")) if patient_data else 0
    )

    Clinical_Stage = st.multiselect("Clinical Stage", ["cT0", "cTx", "cT1a", "cT1b", "cT2a", "cT2b", "cT3a", "cT3b", "cT3c", "cT4", "cN0", "cN1", "M0", "M1"]),
    with st.expander("Clinical Stage Classification"):
        st.write("cT0: No evidence of primary tumor")
        st.write("cTx: Primary tumor cannot be assessed")
        st.write("cT1a: Tumor ≤4 cm in greatest dimension, limited to the kidney")
        st.write("cT1b: Tumor >4 cm but ≤7 cm in greatest dimension, limited to the kidney")
        st.write("cT2a: Tumor confined to kidney, >7 cm but not >10 cm")
        st.write("cT2b: Tumor confined to kidney, >10 cm")
        st.write("cT3a: Tumor grossly extends into the renal vein or its segmental (muscle-containing) branches, invades the pelvicalyceal system, or invades perirenal and/or renal sinus fat but not beyond the Gerota fascia")
        st.write("cT3b: Tumor extends into the vena cava above the diaphragm or invades the wall of the vena cava")
        st.write("cT3c: Tumor extends into the vena cava wall with extension into the vena cava wall")
        st.write("cT4: Tumor invades beyond Gerota's fascia")
        default=safe_get_list(patient_data, "Clinical Stage") if patient_data else []

    Type_of_Confirmatory_procedure = st.radio("Type of Confirmatory procedure", ["Biopsy", "Partial Nephrectomy", "Radical Nephrectomy", "Image Only", "Others"],
        index=["Biopsy", "Partial Nephrectomy", "Radical Nephrectomy", "Image Only", "Others"].index(safe_get(patient_data, "Type_of_Confirmatory_procedure", "Biopsy")) if patient_data else 0
    )
    
    Biopsy_date = st.date_input("Date of Biopsy",
        value=datetime.strptime(safe_get(patient_data, "Surgery_date", "1900-01-01"), "%Y-%m-%d").date() if patient_data else date.today()
    )

    Recurrent_Tumor = st.radio("Recurrent Tumor", ["No", "Yes"]),
    index=["No", "Yes"].index(safe_get(patient_data, "Recurrent_Tumor", "No")) if patient_data else 0
    
    if Recurrent_Tumor == "Yes":
        Recurrence_date = st.date_input("Date of Recurrence",
            value=datetime.strptime(safe_get(patient_data, "Recurrence_date", "1900-01-01"), "%Y-%m-%d").date() if patient_data else date.today()
        )
        Surgery_type = st.radio("Surgery type", ["Partial Nephrectomy", "Radical Nephrectomy", "Others"],
        index=["Partial Nephrectomy", "Radical Nephrectomy", "Others"].index(safe_get(patient_data, "Surgery_type", "Partial Nephrectomy")) if patient_data else 0
        )
        Surgery_date = st.date_input("Date of Surgery",
            value=datetime.strptime(safe_get(patient_data, "Surgery_date", "1900-01-01"), "%Y-%m-%d").date() if patient_data else date.today()
        )
    
    # Systemic Treatment
    st.subheader("Systemic Treatment")
    Systemic_Treatment = st.multiselect("Systemic_Treatment", ["None", "Conventional Chemotherapy", "Target Therapy", "Immunotherapy", "Radioligant", "ADC", "Others"]),
    if Systemic_Treatment : ("None", "Conventional Chemotherapy", "Target Therapy", "Immunotherapy", "Radioligant", "ADC", "Others").index(safe_get(patient_data, "Systemic_Treatment", "None")) if patient_data else 0
    Systemic_Treatment_first_date = st.date_input("First Date of Systemic_Treatment",   
            value=datetime.strptime(safe_get(patient_data, "Systemic_Treatment_first_date", "1900-01-01"), "%Y-%m-%d").date() if patient_data else date.today()
        )
    Systemic_Treatment_last_date = st.date_input("Last Date of Systemic_Treatment",
            value=datetime.strptime(safe_get(patient_data, "Systemic_Treatment_last_date", "1900-01-01"), "%Y-%m-%d").date() if patient_data else date.today()
        )
    default=safe_get_list(patient_data, "Systemic_Treatment") if patient_data else []

    # Treatment Details
    st.subheader("Treatment Details")
    Dose = st.multiselect("Dose", ["26Gy", "35Gy", "40Gy", "30Gy", "Others"],
    default=safe_get_list(patient_data, "Dose") if patient_data else []
    )

    Fractionation = st.multiselect("Fractionation", ["1", "2", "3", "5", "10", "Others"],
    default=safe_get_list(patient_data, "Fractionation") if patient_data else []
    )
    
    st.markdown("<hr style='border: 2px solid #666; margin: 20px 0;'>", unsafe_allow_html=True)

    # Side effects
    st.subheader("Urinary Side Effects")

    Dysuria = st.radio("Dysuria (CTCAE v5)", ["Present", "Absent"])
    
    Cystitis = st.radio("Cystitis (CTCAE v5)", ["None", "I", "II", "III", "IV", "V"])
    with st.expander("Cystitis Classification"):
        st.write("Grade 0: No change")
        st.write("Grade I: Microscopic hematuria; minimal increase in frequency, urgency, dysuria, or nocturia; new onset of incontinence ")
        st.write("Grade II: Moderate hematuria; moderate increase in frequency, urgency, dysuria, nocturia or incontinence; urinary catheter placement or bladder irrigation indicated; limiting instrumental ADL ")     
        st.write("Grade III: Gross hematuria; transfusion, IV medications, or hospitalization indicated; elective invasive intervention indicated ")
        st.write("Grade IV: Life-threatening consequences; urgent invasive intervention indicated ")
        st.write("Grade V: Death")

    Bladder_Perforation = st.radio("Bladder Perforation (CTCAE v5)", ["Absent", "II", "III", "IV", "V"])
    with st.expander("Bladder Perforation Classification"):
        st.write("Absent: No change")
        st.write("Grade II: Invasive intervention not indicated ")
        st.write("Grade III: Symptomatic; medical intervention indicated")
        st.write("Grade IV: Life-threatening consequences; urgent intervention indicated")
        st.write("Grade V: Death")

    Hematuria = st.radio("Hematuria (CTCAE v5)", ["Absent", "I", "II", "III", "IV", "V"])
    with st.expander("Hematuria Classification"):
        st.write("Absent: No change")
        st.write("Grade I: Asymptomatic; clinical or diagnostic observations only; intervention not indicated")
        st.write("Grade II: Symptomatic; urinary catheter or bladder irrigation indicated; limiting instrumental ADL")
        st.write("Grade III: Gross hematuria; transfusion, IV medications, or hospitalization indicated; elective invasive intervention indicated; limiting self care ADL")
        st.write("Grade IV: Life-threatening consequences; urgent invasive intervention indicated")
        st.write("Grade V: Death")

    Urinary_Fistula = st.radio("Urinary Fistula (CTCAE v5)", ["Absent", "II", "III", "IV", "V"])
    with st.expander("Urinary Fistula Classification"):
        st.write("Absent: No change")
        st.write("Grade II: Invasive intervention not indicated ")
        st.write("Grade III: Symptomatic; medical intervention indicated")
        st.write("Grade IV: Life-threatening consequences; urgent intervention indicated")
        st.write("Grade V: Death")

    Urinary_Obstruction = st.radio("Urinary Obstruction (CTCAE v5)", ["Absent", "I", "II", "III", "IV", "V"])
    with st.expander("Urinary Obstruction Classification"):
        st.write("Absent: No change")
        st.write("Grade I: Asymptomatic; clinical or diagnostic observations only; intervention not indicated")
        st.write("Grade II: Symptomatic but no hydronephrosis, sepsis, or renal dysfunction; urethral dilation, urinary or suprapubic catheter indicated")
        st.write("Grade III: Altered organ function (e.g., hydronephrosis or renal dysfunction); invasive intervention indicated")
        st.write("Grade IV: Life-threatening consequences; urgent intervention indicated")
        st.write("Grade V: Death")

    Ureteral_Stenosis = st.radio("Ureteral Stenosis", ["Absent", "Present"])
    if Ureteral_Stenosis == "Present":
        Ureteral_Stenosis_date = st.date_input("Date of Ureteral Stenosis")

    

    # Side Effects - Gastrointestinal
    st.subheader("Gastrointestinal Side Effects")

    Diarrhea = st.radio("Diarrhea (CTCAE v5)", ["Absent", "I", "II", "III", "IV", "V"])
    with st.expander("Diarrhea Classification"):
        st.write("Absent: No change")
        st.write("Grade I: Increase of <4 stools/day over baseline; mild increase in ostomy output compared to baseline")
        st.write("Grade II: Increase of 4-6 stools/day over baseline; moderate increase in ostomy output compared to baseline; limiting instrumental ADL")
        st.write("Grade III: Increase of ≥7 stools/day over baseline; incontinence; limiting self care ADL")
        st.write("Grade IV: Life-threatening consequences; urgent intervention indicated")
        st.write("Grade V: Death")
    
    Nausea = st.radio("Nausea (CTCAE v5)", ["Absent", "I", "II", "III", "IV", "V"])
    with st.expander("Nausea Classification"):
        st.write("Absent: No change")
        st.write("Grade I: Loss of appetite without alteration in eating habits")
        st.write("Grade II: Oral intake decreased without significant weight loss, dehydration, or malnutrition; IV fluids indicated <24 hrs")
        st.write("Grade III: Inadequate oral caloric or fluid intake; tube feeding or TPN indicated")
        st.write("Grade IV: Life-threatening consequences; urgent intervention indicated")
        st.write("Grade V: Death")
    
    Bowel_Perforation = st.radio("Bowel Perforation (CTCAE v5)", ["Absent", "II", "III", "IV", "V"])
    with st.expander("Bowel Perforation Classification"):
        st.write("Absent: No change")
        st.write("Grade II: Invasive intervention not indicated ")
        st.write("Grade III: Symptomatic; medical intervention indicated")
        st.write("Grade IV: Life-threatening consequences; urgent intervention indicated")
        st.write("Grade V: Death")

    Bowel_Obstruction = st.radio("Bowel Obstruction (CTCAE v5)", ["Absent", "I", "II", "III", "IV", "V"])
    with st.expander("Bowel Obstruction Classification"):
        st.write("Absent: No change")
        st.write("Grade I: Asymptomatic; clinical or diagnostic observations only; intervention not indicated")
        st.write("Grade II: Symptomatic; noninvasive intervention indicated")
        st.write("Grade III: Symptomatic; invasive intervention indicated")
        st.write("Grade IV: Life-threatening consequences; urgent intervention indicated")
        st.write("Grade V: Death")

    #Other Side Effects
    st.subheader("Fatigue")

    Fatigue = st.radio("Fatigue", ["None", "I", "II", "III"])
    with st.expander("Fatigue Classification"):
        st.write("Grade 0: No fatigue")
        st.write("Grade I: Mild fatigue; no change in activity")
        st.write("Grade II: Moderate fatigue; limiting instrumental ADL")
        st.write("Grade III: Severe fatigue; limiting self care ADL")

    Overal_tolerance = st.radio("Overall Tolerance", ["Excellent", "Good", "Fair", "Poor"])

    # Recurrence details
    st.subheader("Recurrence Details")
    local_recurrence = st.radio("Local Recurrence", ["No", "Yes"])
    regional_recurrence = st.radio("Regional Recurrence", ["No", "Yes"])
    distant_recurrence = st.radio("Distant Recurrence", ["No", "Yes"])
    death = st.radio("Death", ["No", "Yes"])

    
    time_to_local_recurrence = None
    if local_recurrence == "Yes":
        time_to_local_recurrence = calculate_months(last_radiotherapy_date, st.date_input("Date of Local Recurrence"))

    time_to_regional_recurrence = None
    if regional_recurrence == "Yes":
        time_to_regional_recurrence = calculate_months(last_radiotherapy_date, st.date_input("Date of Regional Recurrence"))

    time_to_distant_recurrence = None
    if distant_recurrence == "Yes":
        time_to_distant_recurrence = calculate_months(last_radiotherapy_date, st.date_input("Date of Distant Recurrence"))

    death_date = None
    if death == "Yes":
        Cancer_related_death = st.radio("Cancer Related Death", ["No", "Yes"])
        time_to_death = calculate_months(last_radiotherapy_date, st.date_input("Date of Death"))

    # Submit button to trigger calculation
    submitted = st.form_submit_button("Calculate")

    if submitted:
        st.session_state.age = datetime.today().year - date_of_birth.year - (
            (datetime.today().month, datetime.today().day) < (date_of_birth.month, date_of_birth.day)
        )
        st.session_state.time_since_treatment = calculate_months(last_radiotherapy_date, follow_up_date)
        st.session_state.time_to_local_recurrence = time_to_local_recurrence if local_recurrence == "Yes" else "N/A"
        st.session_state.time_to_regional_recurrence = time_to_regional_recurrence if regional_recurrence == "Yes" else "N/A"
        st.session_state.time_to_distant_recurrence = time_to_distant_recurrence if distant_recurrence == "Yes" else "N/A"
        st.session_state.time_to_death = time_to_death if death == "Yes" else "N/A"

        st.subheader("Calculated Results:")
        st.write(f"**Calculated Age**: {st.session_state.age} years")
        st.write(f"**Time since last radiotherapy**: {st.session_state.time_since_treatment} months")
        if local_recurrence == "Yes":
            st.write(f"**Time to local recurrence**: {st.session_state.time_to_local_recurrence} months")
        if regional_recurrence == "Yes":
            st.write(f"**Time to regional recurrence**: {st.session_state.time_to_regional_recurrence} months")
        if distant_recurrence == "Yes":
            st.write(f"**Time to distant recurrence**: {st.session_state.time_to_distant_recurrence} months")
        if death == "Yes":
            st.write(f"**Time to death**: {st.session_state.time_to_death} months")

# Save button is placed outside the form so it persists after submission
if st.button("Save Information"):
    if st.session_state.age is None or st.session_state.time_since_treatment is None:
        st.error("Please calculate the age and treatment times before saving.")
    else:
        data = {
            # Patient details
            "MRN": mrn if mrn else "N/A",
            "Date_of_Birth": date_of_birth.strftime("%Y-%m-%d"),
            "Age": st.session_state.age,
            "Date_of_Last_Radiotherapy": last_radiotherapy_date.strftime("%Y-%m-%d"),
            "Follow_up_date": follow_up_date.strftime("%Y-%m-%d"),
            "Follow_up_time": st.session_state.time_since_treatment,
            "Histology": Histology,
            "Grade": Grade,
            "Tumor_Focality": Tumor_Focality,
            "Clinical_Stage": Clinical_Stage,
            "Type_of_Confirmatory_procedure": Type_of_Confirmatory_procedure,
            "Biopsy_date": Biopsy_date.strftime("%Y-%m-%d"),
            "Recurrent_Tumor": Recurrent_Tumor,
            "Recurrence_date": Recurrence_date.strftime("%Y-%m-%d") if Recurrent_Tumor == "Yes" else "N/A",
            "Surgery_type": Surgery_type if Recurrent_Tumor == "Yes" else "N/A",
            "Surgery_date": Surgery_date.strftime("%Y-%m-%d") if Recurrent_Tumor == "Yes" else "N/A",
            # Systemic Treatment
            "Systemic_Treatment": Systemic_Treatment,
            "Systemic_Treatment_first_date": Systemic_Treatment_first_date.strftime("%Y-%m-%d"),
            "Systemic_Treatment_last_date": Systemic_Treatment_last_date.strftime("%Y-%m-%d"),
            # Treatment Details
            "Dose": Dose,
            "Fractionation": Fractionation,
            # Side Effects
            "Fatigue": Fatigue,
            "Dysuria": Dysuria,
            "Cystitis": Cystitis,
            "Bladder_Perforation": Bladder_Perforation,
            "Hematuria": Hematuria,
            "Urinary_Fistula": Urinary_Fistula,
            "Urinary_Obstruction": Urinary_Obstruction,
            "Ureteral_Stenosis": Ureteral_Stenosis,
            "Diarrhea": Diarrhea,
            "Nausea": Nausea,
            "Bowel_Perforation": Bowel_Perforation,
            "Bowel_Obstruction": Bowel_Obstruction,
            "Overal_tolerance": Overal_tolerance,
            # Recurrence Details
            "Local_recurrence": local_recurrence,
            "Time_to_local_recurrence": st.session_state.time_to_local_recurrence if local_recurrence == "Yes" else "N/A",
            "Regional_recurrence": regional_recurrence,
            "Time_to_regional_recurrence": st.session_state.time_to_regional_recurrence if regional_recurrence == "Yes" else "N/A",
            "Distant_recurrence": distant_recurrence,
            "Time_to_distant_recurrence": st.session_state.time_to_distant_recurrence if distant_recurrence == "Yes" else "N/A",
            "Cancer Related Death": Cancer_related_death if death == "Yes" else "N/A",
            "Death": death,
            "time_to_death": st.session_state.time_to_death if death == "Yes" else "N/A",
        }
        save_data(data)
        st.success("Patient data has been successfully saved!")
