import React from 'react';

const DisasterCard = ({ event }) => {
    const getSeverityColor = (severity) => {
        if (!severity) return '';
        // Handle both object (new) and string (legacy) formats
        const s = (typeof severity === 'object' ? severity.level : severity) || '';
        const lowerS = s.toLowerCase();

        if (lowerS.includes('high') || lowerS.includes('severe') || lowerS.includes('major') || lowerS.includes('catastrophic')) return 'severity-high';
        if (lowerS.includes('medium') || lowerS.includes('moderate')) return 'severity-medium';
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
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                    <span className={`card-severity ${getSeverityColor(event.severity)}`}>
                        {typeof event.severity === 'object' ? (event.severity.level || 'Unknown Severity') : (event.severity || 'Unknown Severity')}
                    </span>
                    {typeof event.severity === 'object' && (
                        <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                            <div>Deaths: {event.severity.deaths}</div>
                            <div>Relocations: {event.severity.relocations}</div>
                        </div>
                    )}
                </div>
                <span className="card-source">{event.source}</span>
            </div>
        </div>
    );
};

export default DisasterCard;
