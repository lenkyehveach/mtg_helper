import React, {useState, useEffect} from 'react'; 

const ManaButton = (props) => {
  return (
    <button id={props.name} onClick={props.onClick}>{props.name}</button> 
  )
}

const PhaseButton = (props) => { 
  return (
    <button value={props.name} onClick={props.onClick}>{props.name}</button>
  )
}

const submit = (props) => {
  

} 


// main fucntion 

function QuerySet() {
  const [phase, setPhase] = useState(''); 
  const [mana, setMana] = useState({
    "W": 0,
    "U": 0, 
    "B": 0, 
    "G": 0,
    "R": 0
  });
  
  const phaseChange = (e) => setPhase(e.target.value)

  const manaChange = (e) => {
    const addOne = (initial) => initial + 1
    setMana((prevMana) => ({
      ...prevMana, 
      [e.target.id]: addOne(mana[e.target.id])
    }))
  }

  const manas = ['W', 'U', 'B', 'G', 'R'];
  const manaButtons = manas.map( (m) =>
    <li>
      <ManaButton name={m} onClick={manaChange} />
    </li>
   );

   const reset = () => {
     setMana({
      "W": 0,
      "U": 0, 
      "B": 0, 
      "G": 0,
      "R": 0
    })
    setPhase("")
   }

  const phases = ['pre-combat main', 'combat', 'post-combat', 'ending'];
  const phaseButtons = phases.map( (phase) => 
    <li>
      <PhaseButton name={phase} onClick={phaseChange} />
    </li>
  );

  return (
    <div className="qset">
      <h1>Open mana: {mana.W}W {mana.U}U {mana.B}B {mana.G}G {mana.R}R</h1>
      <ul className="manaBit"> 
        {manaButtons}
      </ul>
      <h1>Current phase {phase}</h1>
      <ul className="phaseBit">
        {phaseButtons}
      </ul>
      <button onClick={reset}>Reset</button>
    </div>
  )
  
}

export default QuerySet;