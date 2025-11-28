import React from 'react';

const DisasterCard = ({ event }) => {
    const getSeverityColor = (severity) => {
        if (!severity) return '';
        const s = severity.toLowerCase();
        if (s.includes('high') || s.includes('severe') || s.includes('major') || s.includes('catastrophic')) return 'severity-high';
        if (s.includes('medium') || s.includes('moderate')) return 'severity-medium';
        return 'severity-low';
    };

    return (
        <div className="disaster-card">
            <div className="card-header">
                <span className="card-type">{event.type}</span>
                <span className="card-date">{event.date}</span>
            </div>
            <h3 className="card-location">{event.location}</h3>
            <p className="card-description">{event.description}</p>
            <div className="card-footer">
                <span className={`card-severity ${getSeverityColor(event.severity)}`}>
                    {event.severity || 'Unknown Severity'}
                </span>
                <span className="card-source">{event.source}</span>
            </div>
        </div>
    );
};

export default DisasterCard;
