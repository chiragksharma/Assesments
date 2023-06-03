import streamlit as st
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration, AutoTokenizer
import itertools
from nltk.corpus import stopwords
import nltk
import easyocr
import torch
import numpy as np
nltk.download('stopwords')

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
reader = easyocr.Reader(['en'])
# set up Streamlit app
st.set_page_config(layout='wide', page_title='Image Hashtag Recommender')

def genrate_caption(image_file):
    image = Image.open(image_file).convert('RGB')
    inputs = processor(image, return_tensors="pt")
    output_ids = model.generate(**inputs)
    output_text = processor.decode(output_ids[0], skip_special_tokens=True)
    return output_text
    
st.title("Image Caption and HashTag Recommender")
image_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if image_file is not None:
    try:
        caption = genrate_caption(image_file)
        if len(caption) > 0:
            st.write(f"Caption : {caption}")
        
        else:
            st.write("No caption found for this image.")
    except Exception as e:
        st.write(f"Error: {e}")

    