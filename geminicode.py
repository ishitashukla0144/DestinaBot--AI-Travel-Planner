import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
import base64


# Set your Gemini API key here
genai.configure(api_key="AIzaSyCVYgy93LXNbxZ2PHBhcCTsxfpaLGsyzGg")

st.set_page_config(page_title="DESTINABOT", layout="wide")


def set_background_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode()
    page_bg_img = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded_image}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)


if "page" not in st.session_state:
    st.session_state["page"] = "home"

if st.session_state["page"] == "home":
    set_background_image(r"C:\\Users\\prasi\\PycharmProjects\\pythonProject1\\travel.jpg")


st.sidebar.title(" About Destinabot")
st.sidebar.info(
    "**AI-Powered Travel Itinerary Generator**\n\n"
    " Customized travel plans based on your preferences.\n\n"
    " Detailed itineraries including activities, food, and transport.\n\n"
    " Download your personalized itinerary as a PDF.\n\n"
    "_Plan your adventure effortlessly!_"
)


# Function to generate itinerary using Gemini
def generate_itinerary(from_location, to_location, days, month, moods, transport, budget_type):
    mood_str = ", ".join(moods)
    transport_str = ", ".join(transport)
    prompt = f"""
    Generate a detailed {days}-day travel itinerary from {from_location} to {to_location} in {month}.
    Preferences:
    - Moods: {mood_str}
    - Preferred transport: {transport_str}
    - Budget type: {budget_type}

    The itinerary should include:
    - Morning, Afternoon, and Evening time slots.
    - Specific places to visit, activities, and food recommendations.
    - Average trip price and daily cost breakdown based on budget type.
    - Accessibility-friendly options for elderly or young travelers.
    """

    try:
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")  # or "gemini-1.5-flash"
        response = model.generate_content([prompt])
        return response.text
    except Exception as e:
        return f"Unable to generate itinerary: {e}"



# Function to create a PDF
def create_pdf(itinerary):
    safe_itinerary = itinerary.replace('₹', 'INR')
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, safe_itinerary)
    return pdf.output(dest='S').encode('latin1')


# Main Streamlit app logic
def main():
    if st.session_state["page"] == "home":
        st.title(" Destinabot Travel Planner")
        st.subheader("Plan your perfect trip effortlessly with AI!")

        from_location = st.text_input("Enter departure location:", value="")
        to_location = st.text_input("Enter destination:", value="")
        days = st.number_input("Enter the number of days (1-15):", min_value=1, max_value=15, value=1)
        month = st.selectbox("Select the month of your trip:", [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"])

        budget_type = st.selectbox("Select your budget type:", ["Economy", "Moderate", "Luxury"])

        moods = st.multiselect("Select your travel mood:",
                               ["Adventure", "Cultural", "Nature", "Romantic", "Relaxation"])
        transport = st.multiselect("Preferred mode of transport:", ["Flight", "Train", "Bus", "Cab"])

        if st.button(" Generate Itinerary"):
            if from_location and to_location:
                itinerary = generate_itinerary(from_location, to_location, days, month, moods, transport, budget_type)
                st.session_state["itinerary"] = itinerary
                st.session_state["page"] = "itinerary"
                st.rerun()
            else:
                st.warning("Please fill in both departure and destination locations.")

    elif st.session_state["page"] == "itinerary":
        st.markdown(
            """
            <style>
            .stApp {
                background-color: white;
            }
            </style>
            """, unsafe_allow_html=True)

        st.title(" Your Destina Itinerary")
        st.markdown(st.session_state["itinerary"])

        pdf_bytes = create_pdf(st.session_state["itinerary"])
        st.download_button(
            label=" Download Itinerary as PDF",
            data=pdf_bytes,
            file_name="Travel_Itinerary.pdf",
            mime="application/pdf"
        )

        if st.button(" Plan Another Trip"):
            st.session_state["page"] = "home"
            st.rerun()


if __name__ == "__main__":
    main()