// Author        : CHAN Cheuk Hei
// Student Name  : CHAN Cheuk Hei
// Student ID    : 57270778
// Usage         : Main - React.js Component [CollapsibleSection.jsx]

import { useState } from "react";

function CollapsibleSection({ title, children, isOpenByDefault = false }) {
    const [isOpen, setIsOpen] = useState(isOpenByDefault);

    // Toggle the collapsed state when clicking the title
    const toggleCollapse = () => {
        setIsOpen(!isOpen);
    };

    return (
        <div>
            {/* Clicking the h3 tag toggles the section */}
            <h3 onClick={toggleCollapse} style={{ cursor: "pointer" }}>
                {title}
                {/* Optional: Add an icon to indicate collapsible state */}
                <span style={{ marginLeft: "10px" }}>{isOpen ? "▼" : "▶"}</span>
            </h3>
            {/* Show children (list) only if section is open */}
            {isOpen && <div>{children}</div>}
        </div>
    );
}

export default CollapsibleSection