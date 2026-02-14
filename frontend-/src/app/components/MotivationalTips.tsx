import { motion } from "motion/react";
import { Lightbulb, Zap, Target, TrendingUp } from "lucide-react";
import { useState, useEffect } from "react";

const tips = [
  {
    icon: Lightbulb,
    title: "Every Expert Started as a Beginner",
    message: "Your journey matters more than your starting point. Keep pushing forward!",
    color: "from-yellow-500 to-orange-500"
  },
  {
    icon: Zap,
    title: "Consistency Beats Perfection",
    message: "Small daily steps compound into extraordinary results over time.",
    color: "from-blue-500 to-cyan-500"
  },
  {
    icon: Target,
    title: "Focus on Your Dream Role",
    message: "You're one decision away from starting your path to success.",
    color: "from-purple-500 to-pink-500"
  },
  {
    icon: TrendingUp,
    title: "Growth is Always Possible",
    message: "No matter where you are now, you can absolutely reach your goals.",
    color: "from-green-500 to-emerald-500"
  }
];

export function MotivationalTips() {
  const [currentTip, setCurrentTip] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTip((prev) => (prev + 1) % tips.length);
    }, 6000);
    return () => clearInterval(timer);
  }, []);

  const tip = tips[currentTip];
  const Icon = tip.icon;

  return (
    <motion.div
      className="w-full mb-8"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
    >
      <div
        className="rounded-2xl p-6 md:p-8 relative overflow-hidden"
        style={{
          background: `linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(59, 130, 246, 0.15) 100%)`,
          border: "1px solid rgba(99, 102, 241, 0.3)",
          boxShadow: "0 0 40px rgba(99, 102, 241, 0.1)",
        }}
      >
        {/* Animated Background Gradient */}
        <motion.div
          className="absolute inset-0 opacity-0"
          animate={{
            boxShadow: [
              "0 0 40px rgba(99, 102, 241, 0.1)",
              "0 0 80px rgba(99, 102, 241, 0.2)",
              "0 0 40px rgba(99, 102, 241, 0.1)",
            ],
          }}
          transition={{ duration: 4, repeat: Infinity }}
        />

        <div className="relative z-10">
          <motion.div
            key={currentTip}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.5 }}
            className="flex items-start space-x-4"
          >
            <div className={`w-12 h-12 rounded-lg bg-gradient-to-br ${tip.color} flex items-center justify-center flex-shrink-0`}>
              <Icon className="w-6 h-6 text-white" />
            </div>
            <div className="flex-1">
              <h3 className="text-lg font-semibold text-white mb-2">{tip.title}</h3>
              <p className="text-gray-300 text-sm md:text-base">{tip.message}</p>
            </div>
          </motion.div>
        </div>

        {/* Tip Indicators */}
        <div className="flex justify-center gap-2 mt-6 relative z-10">
          {tips.map((_, idx) => (
            <motion.button
              key={idx}
              onClick={() => setCurrentTip(idx)}
              className={`w-2 h-2 rounded-full transition-all ${
                idx === currentTip ? "bg-indigo-400 w-6" : "bg-white/30 hover:bg-white/50"
              }`}
              whileHover={{ scale: 1.2 }}
            />
          ))}
        </div>
      </div>
    </motion.div>
  );
}
