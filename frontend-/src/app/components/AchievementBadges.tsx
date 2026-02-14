import { motion } from "motion/react";
import { Star, CheckCircle2, Flame, Award } from "lucide-react";

interface Badge {
  icon: React.ReactNode;
  label: string;
  unlocked: boolean;
  color: string;
}

const badges: Badge[] = [
  {
    icon: <CheckCircle2 className="w-6 h-6" />,
    label: "First Step",
    unlocked: true,
    color: "from-green-500 to-emerald-500"
  },
  {
    icon: <Flame className="w-6 h-6" />,
    label: "On Fire",
    unlocked: false,
    color: "from-orange-500 to-red-500"
  },
  {
    icon: <Star className="w-6 h-6" />,
    label: "Achiever",
    unlocked: false,
    color: "from-yellow-500 to-amber-500"
  },
  {
    icon: <Award className="w-6 h-6" />,
    label: "Champion",
    unlocked: false,
    color: "from-purple-500 to-pink-500"
  }
];

export function AchievementBadges() {
  return (
    <motion.div
      className="w-full mb-8"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, delay: 0.2 }}
    >
      <div className="mb-4">
        <h3 className="text-lg font-semibold text-white">Your Milestones</h3>
        <p className="text-sm text-gray-400">Unlock achievements as you progress</p>
      </div>
      
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {badges.map((badge, idx) => (
          <motion.div
            key={idx}
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5, delay: idx * 0.1 }}
            whileHover={{ scale: 1.05 }}
            className={`relative group`}
          >
            <div
              className={`rounded-2xl p-6 flex flex-col items-center justify-center text-center transition-all ${
                badge.unlocked
                  ? `bg-gradient-to-br ${badge.color} shadow-lg shadow-${badge.color.split(' ')[1]}`
                  : "bg-white/5 border border-white/10"
              }`}
            >
              <motion.div
                animate={badge.unlocked ? { rotate: [0, 360] } : {}}
                transition={{ duration: 0.6, delay: idx * 0.15 }}
                className={`mb-3 ${badge.unlocked ? "text-white" : "text-gray-500"}`}
              >
                {badge.icon}
              </motion.div>
              <p className={`text-xs font-semibold ${badge.unlocked ? "text-white" : "text-gray-400"}`}>
                {badge.label}
              </p>
            </div>

            {/* Unlock Tooltip */}
            {badge.unlocked && (
              <motion.div
                initial={{ opacity: 0 }}
                whileHover={{ opacity: 1 }}
                className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-3 py-2 bg-gray-900 rounded-lg text-xs text-white whitespace-nowrap pointer-events-none"
              >
                ✨ Unlocked!
                <div className="absolute top-full left-1/2 -translate-x-1/2 w-2 h-2 bg-gray-900 rotate-45" />
              </motion.div>
            )}
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
}
