import { motion } from "motion/react";
import { useNavigate } from "react-router";
import { useState } from "react";
import { ConstellationBackground } from "../components/ConstellationBackground";
import { Checkbox } from "../components/ui/checkbox";
import { MotivationalTips } from "../components/MotivationalTips";
import { AchievementBadges } from "../components/AchievementBadges";
import { MotivatedButton } from "../components/MotivatedButton";
import { Sparkles, ArrowRight } from "lucide-react";

export function LoginPage() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [rememberMe, setRememberMe] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleSignIn = (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setTimeout(() => {
      navigate("/setup");
    }, 600);
  };

  return (
    <div className="min-h-screen flex dark">
      {/* LEFT SIDE - Hero Section */}
      <motion.div
        className="hidden lg:flex lg:w-1/2 relative items-center justify-center p-8 lg:p-12"
        initial={{ opacity: 0, x: -50 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.6 }}
      >
        <ConstellationBackground />
        
        <div className="relative z-10 max-w-lg w-full space-y-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3, duration: 0.6 }}
          >
            <div className="flex items-center gap-2 mb-4">
              <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-indigo-600 to-blue-600 flex items-center justify-center">
                <Sparkles className="w-5 h-5 text-white" />
              </div>
              <span className="text-sm font-semibold text-indigo-400">Career Navigator</span>
            </div>
            <h1 className="text-5xl md:text-6xl font-semibold text-white mb-6 leading-tight">
              Your AI Career Co-Pilot
            </h1>
            <p className="text-2xl text-blue-100 mb-4 font-light">
              Plans. Adapts. Evolves With You.
            </p>
            <p className="text-lg text-blue-200/80 leading-relaxed">
              Stop guessing your next step. Let AI map your growth intelligently.
            </p>
          </motion.div>

          {/* Motivational Tips */}
          <MotivationalTips />

          {/* Achievement Badges Preview */}
          <AchievementBadges />
        </div>
      </motion.div>

      {/* RIGHT SIDE - Login Card */}
      <div className="w-full lg:w-1/2 flex items-center justify-center p-6 md:p-12 bg-[#0F172A]">
        <motion.div
          className="w-full max-w-md"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2, duration: 0.6 }}
        >
          {/* Glass Card */}
          <div
            className="rounded-3xl p-8 md:p-10"
            style={{
              background: "rgba(30, 41, 59, 0.6)",
              backdropFilter: "blur(20px)",
              border: "1px solid rgba(255, 255, 255, 0.08)",
              boxShadow:
                "0 0 40px rgba(99, 102, 241, 0.15), inset 0 1px 0 rgba(255, 255, 255, 0.05)",
            }}
          >
            <h2 className="text-3xl font-semibold text-white mb-8">
              Welcome Back
            </h2>

            <form onSubmit={handleSignIn} className="space-y-6">
              {/* Email Input */}
              <div className="relative">
                <input
                  type="email"
                  id="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="peer w-full px-4 pt-6 pb-2 bg-white/5 border border-white/10 rounded-2xl text-white placeholder-transparent focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
                  placeholder="Email"
                  required
                />
                <label
                  htmlFor="email"
                  className="absolute left-4 top-2 text-xs text-gray-400 transition-all peer-placeholder-shown:text-base peer-placeholder-shown:top-4 peer-focus:top-2 peer-focus:text-xs peer-focus:text-indigo-400"
                >
                  Email
                </label>
              </div>

              {/* Password Input */}
              <div className="relative">
                <input
                  type="password"
                  id="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="peer w-full px-4 pt-6 pb-2 bg-white/5 border border-white/10 rounded-2xl text-white placeholder-transparent focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
                  placeholder="Password"
                  required
                />
                <label
                  htmlFor="password"
                  className="absolute left-4 top-2 text-xs text-gray-400 transition-all peer-placeholder-shown:text-base peer-placeholder-shown:top-4 peer-focus:top-2 peer-focus:text-xs peer-focus:text-indigo-400"
                >
                  Password
                </label>
              </div>

              {/* Remember Me & Forgot Password */}
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <Checkbox
                    id="remember"
                    checked={rememberMe}
                    onCheckedChange={(checked) => setRememberMe(checked === true)}
                  />
                  <label
                    htmlFor="remember"
                    className="text-sm text-gray-300 cursor-pointer"
                  >
                    Remember me
                  </label>
                </div>
                <button
                  type="button"
                  className="text-sm text-indigo-400 hover:text-indigo-300 transition-colors"
                >
                  Forgot password?
                </button>
              </div>

              {/* Sign In Button */}
              <MotivatedButton
                onClick={handleSignIn}
                motivationalText="Let's start your journey! 🚀"
              >
                Sign In
                <ArrowRight className="w-4 h-4 ml-2" />
              </MotivatedButton>

              {/* Create Account Button */}
              <motion.button
                type="button"
                onClick={() => navigate("/setup")}
                className="w-full py-4 px-6 bg-transparent border-2 border-white/10 text-white rounded-2xl font-semibold hover:border-indigo-500/50 hover:bg-white/5 transition-all group"
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                <span className="flex items-center justify-center gap-2">
                  Create Account
                  <motion.span
                    animate={{ x: [0, 4, 0] }}
                    transition={{ duration: 1.5, repeat: Infinity }}
                  >
                    →
                  </motion.span>
                </span>
              </motion.button>
            </form>
          </div>

          {/* Mobile Hero Text */}
          <motion.div
            className="lg:hidden mt-8 text-center"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.6 }}
          >
            <h3 className="text-2xl font-semibold text-white mb-2">
              Your AI Career Co-Pilot
            </h3>
            <p className="text-blue-200/60">
              Plans. Adapts. Evolves With You.
            </p>
          </motion.div>
        </motion.div>
      </div>
    </div>
  );
}