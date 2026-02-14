import { motion } from "motion/react";
import { useEffect, useState } from "react";

interface Star {
  id: number;
  x: number;
  y: number;
  size: number;
  opacity: number;
  twinkleDelay: number;
}

interface ShootingStar {
  id: number;
  startX: number;
  startY: number;
  angle: number;
  duration: number;
  delay: number;
}

interface Constellation {
  stars: { x: number; y: number }[];
  connections: [number, number][];
}

export function ConstellationBackground() {
  const [stars, setStars] = useState<Star[]>([]);
  const [shootingStars, setShootingStars] = useState<ShootingStar[]>([]);
  const [constellations, setConstellations] = useState<Constellation[]>([]);

  useEffect(() => {
    // Generate static stars
    const generatedStars: Star[] = Array.from({ length: 200 }, (_, i) => ({
      id: i,
      x: Math.random() * 100,
      y: Math.random() * 100,
      size: Math.random() * 2 + 1,
      opacity: Math.random() * 0.5 + 0.3,
      twinkleDelay: Math.random() * 3,
    }));
    setStars(generatedStars);

    // Generate constellations
    const generatedConstellations: Constellation[] = Array.from({ length: 8 }, () => {
      const numStars = Math.floor(Math.random() * 3) + 3;
      const baseX = Math.random() * 80 + 10;
      const baseY = Math.random() * 80 + 10;
      
      const constellationStars = Array.from({ length: numStars }, () => ({
        x: baseX + (Math.random() - 0.5) * 20,
        y: baseY + (Math.random() - 0.5) * 20,
      }));

      const connections: [number, number][] = [];
      for (let i = 0; i < numStars - 1; i++) {
        connections.push([i, i + 1]);
      }
      // Sometimes connect back to create shapes
      if (Math.random() > 0.5 && numStars > 3) {
        connections.push([numStars - 1, 0]);
      }

      return { stars: constellationStars, connections };
    });
    setConstellations(generatedConstellations);

    // Generate shooting stars periodically
    const createShootingStar = () => {
      const newShootingStar: ShootingStar = {
        id: Date.now(),
        startX: Math.random() * 100,
        startY: Math.random() * 50,
        angle: Math.random() * 45 + 20, // 20-65 degrees
        duration: Math.random() * 1 + 1.5,
        delay: 0,
      };
      
      setShootingStars((prev) => [...prev, newShootingStar]);
      
      setTimeout(() => {
        setShootingStars((prev) => prev.filter((s) => s.id !== newShootingStar.id));
      }, (newShootingStar.duration + newShootingStar.delay) * 1000 + 500);
    };

    // Create shooting stars at random intervals
    const intervals: NodeJS.Timeout[] = [];
    const createInterval = () => {
      const delay = Math.random() * 3000 + 2000; // 2-5 seconds
      const timeout = setTimeout(() => {
        createShootingStar();
        createInterval();
      }, delay);
      intervals.push(timeout);
    };
    
    createInterval();
    createInterval(); // Start with two concurrent shooting star generators

    return () => {
      intervals.forEach(clearTimeout);
    };
  }, []);

  return (
    <div className="absolute inset-0 overflow-hidden">
      {/* Gradient Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-indigo-950 via-slate-900 to-blue-950" />
      
      {/* Animated Nebula Clouds */}
      <motion.div
        className="absolute top-0 right-0 w-[800px] h-[800px] bg-indigo-600/20 rounded-full filter blur-[120px]"
        animate={{
          x: [0, 100, 0],
          y: [0, 150, 0],
          scale: [1, 1.3, 1],
        }}
        transition={{
          duration: 25,
          repeat: Infinity,
          ease: "easeInOut",
        }}
      />
      <motion.div
        className="absolute bottom-0 left-0 w-[600px] h-[600px] bg-blue-600/20 rounded-full filter blur-[100px]"
        animate={{
          x: [0, -100, 0],
          y: [0, -100, 0],
          scale: [1, 1.2, 1],
        }}
        transition={{
          duration: 20,
          repeat: Infinity,
          ease: "easeInOut",
        }}
      />

      {/* Static Stars with Twinkling */}
      <svg className="absolute inset-0 w-full h-full">
        {stars.map((star) => (
          <motion.circle
            key={star.id}
            cx={`${star.x}%`}
            cy={`${star.y}%`}
            r={star.size}
            fill="white"
            initial={{ opacity: star.opacity }}
            animate={{ 
              opacity: [star.opacity, star.opacity * 0.3, star.opacity],
              scale: [1, 0.8, 1]
            }}
            transition={{
              duration: 3,
              repeat: Infinity,
              delay: star.twinkleDelay,
              ease: "easeInOut",
            }}
          />
        ))}

        {/* Constellations */}
        <defs>
          <linearGradient id="constellationGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style={{ stopColor: "#6366F1", stopOpacity: 0.4 }} />
            <stop offset="100%" style={{ stopColor: "#3B82F6", stopOpacity: 0.2 }} />
          </linearGradient>
        </defs>
        
        {constellations.map((constellation, cIndex) => (
          <g key={cIndex}>
            {/* Constellation lines */}
            {constellation.connections.map(([start, end], lineIndex) => (
              <motion.line
                key={`${cIndex}-${lineIndex}`}
                x1={`${constellation.stars[start].x}%`}
                y1={`${constellation.stars[start].y}%`}
                x2={`${constellation.stars[end].x}%`}
                y2={`${constellation.stars[end].y}%`}
                stroke="url(#constellationGradient)"
                strokeWidth="1"
                initial={{ opacity: 0 }}
                animate={{ opacity: [0.3, 0.6, 0.3] }}
                transition={{
                  duration: 4,
                  repeat: Infinity,
                  delay: cIndex * 0.5,
                  ease: "easeInOut",
                }}
              />
            ))}
            
            {/* Constellation stars */}
            {constellation.stars.map((star, sIndex) => (
              <motion.circle
                key={`${cIndex}-star-${sIndex}`}
                cx={`${star.x}%`}
                cy={`${star.y}%`}
                r="2.5"
                fill="#6366F1"
                initial={{ opacity: 0.4 }}
                animate={{ 
                  opacity: [0.4, 0.8, 0.4],
                  r: [2.5, 3, 2.5]
                }}
                transition={{
                  duration: 3,
                  repeat: Infinity,
                  delay: cIndex * 0.5 + sIndex * 0.2,
                  ease: "easeInOut",
                }}
              />
            ))}
          </g>
        ))}
      </svg>

      {/* Shooting Stars */}
      {shootingStars.map((shootingStar) => {
        const endX = shootingStar.startX + Math.cos((shootingStar.angle * Math.PI) / 180) * 30;
        const endY = shootingStar.startY + Math.sin((shootingStar.angle * Math.PI) / 180) * 30;
        
        return (
          <motion.div
            key={shootingStar.id}
            className="absolute"
            style={{
              left: `${shootingStar.startX}%`,
              top: `${shootingStar.startY}%`,
            }}
            initial={{ x: 0, y: 0, opacity: 0 }}
            animate={{
              x: `${endX - shootingStar.startX}vw`,
              y: `${endY - shootingStar.startY}vh`,
              opacity: [0, 1, 1, 0],
            }}
            transition={{
              duration: shootingStar.duration,
              delay: shootingStar.delay,
              ease: "easeOut",
            }}
          >
            <div
              className="relative"
              style={{
                transform: `rotate(${shootingStar.angle}deg)`,
              }}
            >
              {/* Shooting star trail */}
              <div
                className="h-[2px] bg-gradient-to-r from-transparent via-white to-white rounded-full"
                style={{
                  width: "80px",
                  boxShadow: "0 0 10px rgba(255, 255, 255, 0.8), 0 0 20px rgba(99, 102, 241, 0.6)",
                }}
              />
              {/* Shooting star head */}
              <div
                className="absolute right-0 top-1/2 -translate-y-1/2 w-2 h-2 bg-white rounded-full"
                style={{
                  boxShadow: "0 0 15px rgba(255, 255, 255, 1), 0 0 30px rgba(99, 102, 241, 0.8)",
                }}
              />
            </div>
          </motion.div>
        );
      })}
    </div>
  );
}
