import React, { useState } from 'react';
import { generateContent } from '../services/aiService';

function BannerGenerator({ onContentGenerated }) {
  const [formData, setFormData] = useState({
    productImages: [],
    promotionalOffer: '',
    colorPalette: '',
    theme: '',
    outputType: 'banner',
    size: '1200x628',
    resolution: '72',
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
    <form onSubmit={handleSubmit} className="banner-generator-form">
      <div className="form-group">
        <label htmlFor="productImages">Product Images</label>
        <input
          id="productImages"
          type="file"
          multiple
          accept="image/*"
          onChange={handleImageUpload}
        />
      </div>
      <div className="form-group">
        <label htmlFor="promotionalOffer">Promotional Offer</label>
        <input
          id="promotionalOffer"
          type="text"
          name="promotionalOffer"
          placeholder="Details of the sale, discount, or special offer"
          onChange={handleInputChange}
        />
      </div>
      <div className="form-group">
        <label htmlFor="colorPalette">Color Palette</label>
        <input
          id="colorPalette"
          type="text"
          name="colorPalette"
          placeholder="Comma-separated colors"
          onChange={handleInputChange}
        />
      </div>
      <div className="form-group">
        <label htmlFor="theme">Theme</label>
        <input
          id="theme"
          type="text"
          name="theme"
          placeholder="e.g., Diwali, Independence Day"
          onChange={handleInputChange}
        />
      </div>
      <div className="form-group">
        <label htmlFor="outputType">Output Type</label>
        <select id="outputType" name="outputType" onChange={handleInputChange}>
          <option value="banner">Banner</option>
          <option value="video">Video</option>
        </select>
      </div>
      <div className="form-group">
        <label htmlFor="size">Size</label>
        <select id="size" name="size" onChange={handleInputChange} value={formData.size}>
          <option value="1200x628">1200x628 (Facebook/LinkedIn)</option>
          <option value="1080x1080">1080x1080 (Instagram)</option>
          <option value="1024x512">1024x512 (Twitter)</option>
          <option value="851x315">851x315 (Facebook Cover)</option>
          <option value="custom">Custom</option>
        </select>
        {formData.size === 'custom' && (
          <input
            type="text"
            name="customSize"
            placeholder="Width x Height"
            onChange={handleInputChange}
          />
        )}
      </div>
      <div className="form-group">
        <label htmlFor="resolution">Resolution (DPI)</label>
        <select id="resolution" name="resolution" onChange={handleInputChange} value={formData.resolution}>
          <option value="72">72 DPI (Web)</option>
          <option value="150">150 DPI (Medium Quality)</option>
          <option value="300">300 DPI (Print Quality)</option>
        </select>
      </div>
      <button type="submit" className="generate-button">Generate Content</button>
    </form>
  );
}

export default BannerGenerator;