import React from 'react';

const GlassCard: React.FC = () => {
  return (
    <div className="max-w-sm mx-auto p-6 rounded-xl shadow-lg bg-white bg-opacity-10 backdrop-filter backdrop-blur-lg border border-gray-200 border-opacity-30">
      <h1 className="text-2xl font-bold text-white mb-4">Glass UI Card</h1>
      <p className="text-gray-100">
        This is a beautiful glass effect card created with React and Tailwind CSS.
        The backdrop-blur utility makes the background behind this element blurred.
      </p>
      <button className="mt-4 bg-white bg-opacity-20 hover:bg-opacity-30 text-white font-semibold py-2 px-4 rounded-lg transition duration-300">
        Learn More
      </button>
    </div>
  );
};

export default GlassCard;