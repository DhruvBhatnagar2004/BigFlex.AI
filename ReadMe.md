# BigBasket AI-Powered Dynamic Banner and Video Generator

## 🚀 Project Overview

Welcome to the BigBasket AI-Powered Dynamic Banner and Video Generator! This innovative project revolutionizes promotional content creation for e-commerce platforms, specifically tailored for BigBasket's marketing needs. By leveraging cutting-edge AI technologies, we automate and enhance the process of generating eye-catching banners and videos for various promotional campaigns.

## 🎯 Problem Statement

In the fast-paced world of e-commerce, creating engaging and personalized promotional content at scale is a significant challenge. BigBasket needs a solution that can:

- Rapidly generate high-quality banners and videos for multiple products and offers
- Maintain brand consistency across all promotional materials
- Adapt to various themes and seasonal events
- Optimize content for different platforms and formats

## 💡 Our Solution

Our AI-powered system takes the following inputs:

- Product Images: Multiple images showcasing products
- Promotional Offer Details: Sale information, discounts, and special offers
- Color Palette: Brand-specific colors for consistency
- Theme: Festive or event-based themes (e.g., Diwali, Independence Day)
- Output Specifications: Desired size, resolution, and format (banner or video)

And produces:

- Dynamic, visually appealing banners
- Engaging promotional videos
- Content optimized for various platforms and devices

## 🛠️ Key Features

1. **AI-Powered Background Generation**: Utilizes advanced diffusion models to create contextually relevant backgrounds for product images.
2. **Intelligent Text Generation**: Employs Google's Gemini AI to craft compelling and concise promotional copy.
3. **Dynamic Layout Engine**: Automatically arranges elements (images, text, logos) in multiple appealing layouts.
4. **Theme-Based Customization**: Adapts designs to match seasonal events and festivities.
5. **Multi-Format Output**: Generates both static banners and dynamic video content.
6. **Brand Consistency**: Ensures all generated content adheres to BigBasket's brand guidelines.

## 🚀 Technologies Used

- Python
- PyTorch
- Diffusers library
- Google Generative AI (Gemini)
- Pillow (PIL) for image processing
- Gradio for user interface

## 📊 Impact and Benefits

- **Time Efficiency**: Reduces banner and video creation time from hours to minutes.
- **Cost Reduction**: Minimizes the need for large design teams for promotional content.
- **Scalability**: Easily scales to handle thousands of products and offers simultaneously.
- **Consistency**: Ensures brand coherence across all generated content.
- **Personalization**: Enables creation of tailored promotions for different customer segments.

## 🏆 Why This Project Stands Out

1. **Innovation**: Combines multiple AI technologies for a comprehensive solution.
2. **Practical Application**: Solves a real-world problem for a major e-commerce player.
3. **Scalability**: Designed to handle large-scale operations of BigBasket.
4. **Versatility**: Adaptable to various promotional needs and themes.
5. **User-Friendly**: Intuitive interface makes it accessible to marketing teams.

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/bigbasket-ai-promo-generator.git
   cd bigbasket-ai-promo-generator
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

   If you prefer to install packages individually, you can use the following commands:

   ```bash
   pip install torch
   pip install diffusers
   pip install google-generativeai
   pip install Pillow
   pip install gradio
   pip install transparent-background
   ```

4. Set up your Google API key:
   ```bash
   export GOOGLE_API_KEY='your_api_key_here'
   ```
   On Windows, use `set` instead of `export`.

### Usage

1. Run the background generation script:
   ```bash
   python BgGeneratorWithCPU.py
   ```

2. Run the promotional image generator:
   ```bash
   python promoImageGenerator.py
   ```

3. Access the Gradio interface by opening the URL provided in the console output.

