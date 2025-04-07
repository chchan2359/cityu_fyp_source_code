// Author        : CHAN Cheuk Hei
// Student Name  : CHAN Cheuk Hei
// Student ID    : 57270778
// Usage         : Main - React.js Component [Card.jsx]

function Card({title = "TEMP TITLE", children}) {
    return (
        <div className="card">
            <h2>{title}</h2>
            <hr></hr>
            {children && <div>{children}</div>}
        </div>
    );
}

export default Card;