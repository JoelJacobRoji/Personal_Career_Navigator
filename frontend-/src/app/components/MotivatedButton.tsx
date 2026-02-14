import { motion } from "motion/react";
import { Sparkles } from "lucide-react";
import { useState } from "react";

interface MotivatedButtonProps {
  children: React.ReactNode;
  onClick?: () => void;
  variant?: "primary" | "secondary";
  size?: "sm" | "md" | "lg";
  showSparkles?: boolean;
  motivationalText?: string;
}

export function MotivatedButton({
  children,
  onClick,
  variant = "primary",
  size = "md",
  showSparkles = true,
  motivationalText = "You've got this! 🚀"
}: MotivatedButtonProps) {
  const [showMotivation, setShowMotivation] = useState(false);

  const sizeClasses = {
    sm: "py-2 px-4 text-sm",
    md: "py-4 px-6 text-base",
    lg: "py-5 px-8 text-lg"
  };

  const variantClasses = {
    primary: "bg-gradient-to-r from-indigo-600 to-blue-600 text-white",
    secondary: "bg-transparent border-2 border-white/20 text-white hover:border-indigo-500/50 hover:bg-white/5"
  };

  return (
    <div className="relative">
      <motion.button
        onClick={() => {
          setShowMotivation(true);
          setTimeout(() => setShowMotivation(false), 2000);
          onClick?.();
        }}
        className={`w-full ${sizeClasses[size]} ${variantClasses[variant]} rounded-2xl font-semibold transition-all relative overflow-hidden group`}
        whileHover={{ scale: 1.02, y: -2 }}
        whileTap={{ scale: 0.98 }}
      >
        <span className="relative z-10 flex items-center justify-center gap-2">
          {showSparkles && <Sparkles className="w-4 h-4" />}
          {children}
        </span>
        <div
          className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity"
          style={{
            boxShadow: "0 0 40px rgba(99, 102, 241, 0.8)",
          }}
        />
      </motion.button>

      {/* Motivational Message */}
      <motion.div
        initial={{ opacity: 0, scale: 0, y: 10 }}
        animate={showMotivation ? { opacity: 1, scale: 1, y: -10 } : { opacity: 0, scale: 0, y: 10 }}
        transition={{ duration: 0.3 }}
        className="absolute top-full left-1/2 -translate-x-1/2 mt-2 px-4 py-2 bg-white/10 backdrop-blur-md rounded-full border border-white/20 text-sm text-white whitespace-nowrap pointer-events-none"
      >
        {motivationalText}
      </motion.div>
    </div>
  );
}
