import streamlit as st
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.svm import LinearSVC

# 1. Page Configuration
st.set_page_config(page_title="Theseus Filter", page_icon="⚖️", layout="centered")

# 2. Cache the heavy lifting so it doesn't reload on every button click
@st.cache_resource
def load_system():
    model = SentenceTransformer('all-mpnet-base-v2')
    # Hardcoded contrastive dataset for the demo (Moral Ambiguity Axis)
    positive = ["The choice was grey, full of uncertainty and unresolved tension.", 
                "He accepted the contradiction of his own nature."]
    negative = ["He knew with pure certainty that he was the hero.", 
                "Everything resolved perfectly in the end."]
    
    X = model.encode(positive + negative)
    y = np.array([1, 1, 0, 0])
    svm = LinearSVC(C=1.0, dual="auto").fit(X, y)
    v_hat = svm.coef_[0] / np.linalg.norm(svm.coef_[0])
    
    return model, v_hat

model, v_hat = load_system()

# 3. The UI
st.title("The Theseus Filter")
st.markdown("### AI-Mediated Identity Prototyping Interface")
st.divider()

declaration = st.text_area("Identity Declaration (Anchor)", placeholder="Define your aesthetic and moral commitments here...")
proposal = st.text_area("Explorer Proposal", placeholder="Paste the generative AI output here...")

# 4. The Protocol Execution
if st.button("Analyze Axiological Drift", type="primary"):
    if declaration and proposal:
        with st.spinner("Computing subspace projection..."):
            # Compute signatures
            z_A = np.dot(model.encode(declaration), v_hat)
            z_E = np.dot(model.encode(proposal), v_hat)
            delta_axio = float(abs(z_A - z_E))
            
        # The Variable Autonomy Interface (VAI) Logic
        # Threshold empirically calibrated to 0.11 based on pilot vector space mapping
        if delta_axio > 0.11:  
            st.error(r"**Axiological Friction Detected!**" + "\n\n" + r"Drift Score ($\delta_{\text{axio}}$): " + f"{delta_axio:.4f}")
            st.markdown("The proposal diverges from your anchor values. Please explicitly endorse a resolution:")
            
            # Autonomy Dial choices
            col1, col2, col3 = st.columns(3)
            with col1:
                st.button("Anchor-Dominant", use_container_width=True)
            with col2:
                st.button("Balanced (Merge)", use_container_width=True)
            with col3:
                st.button("Explorer-Dominant", use_container_width=True)
        else:
            st.success(r"**Pass: Output Endorsed.**" + "\n\n" + r"Drift Score ($\delta_{\text{axio}}$): " + f"{delta_axio:.4f}" + " is within acceptable limits.")
    else:
        st.warning("Please provide both an Anchor and a Proposal to run the protocol.")