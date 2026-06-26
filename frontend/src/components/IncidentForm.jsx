import React, { useState } from 'react';

const IncidentForm = ({ onSubmit, isLoading }) => {
  const [formData, setFormData] = useState({
    customer_id: 'CUST-12345',
    incident_type: 'Suspicious Transfer',
    amount: 15000.00,
    currency: 'USD',
    country: 'US',
    device: 'Mobile App',
    beneficiary_status: 'New',
    description: 'User initiated a large transfer to a new beneficiary in a high-risk jurisdiction.'
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'amount' ? parseFloat(value) || 0 : value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <div className="card">
      <h2>Report Financial Incident</h2>
      <form onSubmit={handleSubmit}>
        <div className="grid-2">
          <div className="form-group">
            <label htmlFor="customer_id">Customer ID</label>
            <input type="text" id="customer_id" name="customer_id" className="form-control" value={formData.customer_id} onChange={handleChange} required />
          </div>
          <div className="form-group">
            <label htmlFor="incident_type">Incident Type</label>
            <input type="text" id="incident_type" name="incident_type" className="form-control" value={formData.incident_type} onChange={handleChange} required />
          </div>
          <div className="form-group">
            <label htmlFor="amount">Amount</label>
            <input type="number" step="0.01" id="amount" name="amount" className="form-control" value={formData.amount} onChange={handleChange} required />
          </div>
          <div className="form-group">
            <label htmlFor="currency">Currency</label>
            <input type="text" id="currency" name="currency" className="form-control" value={formData.currency} onChange={handleChange} required />
          </div>
          <div className="form-group">
            <label htmlFor="country">Country</label>
            <input type="text" id="country" name="country" className="form-control" value={formData.country} onChange={handleChange} required />
          </div>
          <div className="form-group">
            <label htmlFor="device">Device</label>
            <input type="text" id="device" name="device" className="form-control" value={formData.device} onChange={handleChange} required />
          </div>
          <div className="form-group">
            <label htmlFor="beneficiary_status">Beneficiary Status</label>
            <input type="text" id="beneficiary_status" name="beneficiary_status" className="form-control" value={formData.beneficiary_status} onChange={handleChange} required />
          </div>
        </div>
        <div className="form-group">
          <label htmlFor="description">Description</label>
          <textarea id="description" name="description" className="form-control" rows="3" value={formData.description} onChange={handleChange} required></textarea>
        </div>
        <button type="submit" className="btn btn-primary" disabled={isLoading}>
          {isLoading ? (
            <>
              <span className="loading-spinner" style={{ marginRight: '8px', width: '1rem', height: '1rem' }}></span>
              Analyzing...
            </>
          ) : 'Analyze Incident'}
        </button>
      </form>
    </div>
  );
};

export default IncidentForm;
