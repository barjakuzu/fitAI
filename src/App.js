import React, { useState } from "react";
import PlanForm from "./Planform.js";

function App() {
  const [plan, setPlan] = useState("");

  return (
    <div className="App">
      <h1>Personalized Workout and Diet Plan Generator</h1>
      <PlanForm setPlan={setPlan} />
      {plan && (
        <div>
          <h2>Generated Plan:</h2>
          <p>{plan}</p>
        </div>
      )}
    </div>
  );
}

export default App;
