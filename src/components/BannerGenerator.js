import React, { useState } from 'react';
import { generateContent } from '../services/aiService';

function BannerGenerator({ onContentGenerated }) {
  const [formData, setFormData] = useState({
    productImages: [],
    promotionalOffer: '',
    colorPalette: '',
    theme: '',
    outputType: 'banner',
    size: '',
    resolution: '',
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleImageUpload = (e) => {
    const files = Array.from(e.target.files);
    setFormData({ ...formData, productImages: files });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const generatedContent = await generateContent(formData);
      onContentGenerated(generatedContent);
    } catch (error) {
      console.error('Error generating content:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="file"
        multiple
        accept="image/*"
        onChange={handleImageUpload}
      />
      <input
        type="text"
        name="promotionalOffer"
        placeholder="Promotional Offer"
        onChange={handleInputChange}
      />
      <input
        type="text"
        name="colorPalette"
        placeholder="Color Palette (comma-separated)"
        onChange={handleInputChange}
      />
      <input
        type="text"
        name="theme"
        placeholder="Theme"
        onChange={handleInputChange}
      />
      <select name="outputType" onChange={handleInputChange}>
        <option value="banner">Banner</option>
        <option value="video">Video</option>
      </select>
      <input
        type="text"
        name="size"
        placeholder="Size (e.g., 1200x628)"
        onChange={handleInputChange}
      />
      <input
        type="text"
        name="resolution"
        placeholder="Resolution (e.g., 72dpi)"
        onChange={handleInputChange}
      />
      <button type="submit">Generate Content</button>
    </form>
  );
}

export default BannerGenerator;