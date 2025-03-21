import streamlit as st
import pandas as pd
import prince
import matplotlib.pyplot as plt
import io

def run_correspondence_analysis(data):
    ca = prince.CA(n_components=2)
    ca = ca.fit(data)
    
    row_coords = ca.row_coordinates(data)
    col_coords = ca.column_coordinates(data)
    
    return row_coords, col_coords

def plot_ca(row_coords, col_coords):
    fig, ax = plt.subplots(figsize=(8, 6))
    
    ax.scatter(row_coords.iloc[:, 0], -row_coords.iloc[:, 1], marker='o', color='blue', label="Flavors")
    for i, txt in enumerate(row_coords.index):
        ax.annotate(txt, (row_coords.iloc[i, 0], -row_coords.iloc[i, 1]), fontsize=9)
    
    ax.scatter(col_coords.iloc[:, 0], -col_coords.iloc[:, 1], marker='^', color='red', label="Brands")
    for i, txt in enumerate(col_coords.index):
        ax.annotate(txt, (col_coords.iloc[i, 0], -col_coords.iloc[i, 1]), fontsize=10, fontweight='bold')
    
    ax.set_title("Correspondence Analysis (CA) - Flavors and Brands", fontsize=12)
    ax.set_xlabel("Dimension 1")
    ax.set_ylabel("Dimension 2 (Flipped)")
    ax.legend()
    plt.grid(True)
    
    return fig

def main():
    st.title("Correspondence Analysis (CA) Tool")
    st.write("Upload a CSV file containing beverage flavor profiles, and this tool will perform Correspondence Analysis and visualize the results.")
    
    uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])
    if uploaded_file is not None:
        try:
            data = pd.read_csv(uploaded_file, index_col=0)
            st.write("### Preview of Data:")
            st.dataframe(data)
            
            row_coords, col_coords = run_correspondence_analysis(data)
            
            st.write("### Correspondence Analysis Results:")
            st.write("#### Row Coordinates (Flavors):")
            st.dataframe(row_coords)
            st.write("#### Column Coordinates (Brands):")
            st.dataframe(col_coords)
            
            fig = plot_ca(row_coords, col_coords)
            st.pyplot(fig)
            
            # Prepare results for download
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                row_coords.to_excel(writer, sheet_name='Flavors')
                col_coords.to_excel(writer, sheet_name='Brands')
                writer.close()
            output.seek(0)
            
            st.download_button(
                label="Download Results (Excel)",
                data=output,
                file_name="correspondence_analysis_results.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        except Exception as e:
            st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
