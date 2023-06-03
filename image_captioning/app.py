import streamlit as st
import os
import cohere
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration, AutoTokenizer
import itertools
from nltk.corpus import stopwords
import nltk
import easyocr
import torch
import numpy as np
nltk.download('stopwords')

COHERE_API_KEY = os.getenv('COHERE_API_KEY')
co_client = cohere.Client(COHERE_API_KEY)


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
    
st.title("Image Caption and HashTag Generator")
image_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

def creative_caption(text):
    return co_client.generate(prompt=f"Write some trendy, catchy, exciting, innovative, captivating, creative and engaging instagram captions for the following prompt - {text}").generations[0].text


def caption_hashtags(text):
    return co_client.generate(prompt=f"Write 10 trendy instagram hashtags for the following prompt - {text}").generations[0].text

if image_file is not None:
    try:
        caption = genrate_caption(image_file)
        caption_text = creative_caption(caption)
        hashtags = caption_hashtags(caption)
        if len(caption) > 0:
            st.write(f"Caption : {caption}")
            st.write(f"Creative Caption : {caption_text}")
            st.write(f"Creative hashtags : {hashtags}")
        
        else:
            st.write("No caption found for this image.")
    except Exception as e:
        st.write(f"Error: {e}")    
    
