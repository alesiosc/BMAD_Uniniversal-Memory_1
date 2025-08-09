import React from 'react';
import modelData from '../../data/modelComparisons.json';

interface ModelComparison {
  name: string;
  pros: string[];
  cons: string[];
}

const ModelCard: React.FC<{ model: ModelComparison }> = ({ model }) => {
  return (
    <div className="bg-gray-800 p-6 rounded-lg border border-gray-700">
      <h3 className="text-lg font-bold text-white mb-4">{model.name}</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <h4 className="font-semibold text-green-400 mb-2">Pros</h4>
          <ul className="list-disc list-inside space-y-1 text-gray-300">
            {model.pros.map((pro, index) => <li key={index}>{pro}</li>)}
          </ul>
        </div>
        <div>
          <h4 className="font-semibold text-red-400 mb-2">Cons</h4>
          <ul className="list-disc list-inside space-y-1 text-gray-300">
            {model.cons.map((con, index) => <li key={index}>{con}</li>)}
          </ul>
        </div>
      </div>
    </div>
  );
};


export const ModelComparisonView: React.FC = () => {
  return (
    <div className="h-full overflow-y-auto p-4 md:p-6">
       <h2 className="text-2xl font-bold text-white mb-6">AI Model Comparison</h2>
       <div className="space-y-6">
        {(modelData as ModelComparison[]).map(model => (
          <ModelCard key={model.name} model={model} />
        ))}
       </div>
    </div>
  );
};