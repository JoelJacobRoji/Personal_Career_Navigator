"""
GitHub Profile Analyzer - Extract skills from GitHub repositories
"""

import os
from collections import Counter
from typing import Dict, Set, Any
from pathlib import Path
from collections import Counter


from github import Github, Auth
from github.GithubException import GithubException

# Import config
import sys
sys.path.append(str(Path(__file__).parent.parent))
from config import Config


class GitHubAnalyzer:
    """Analyze GitHub profile to extract skills"""
    
    def __init__(self, token: str = None):
        print("🔧 Initializing GitHub Analyzer...")
        
        github_token = token or Config.GITHUB_TOKEN
        
        if not github_token:
            print("⚠️  WARNING: GITHUB_TOKEN not found")
            print("   GitHub API has rate limits without authentication")
            self.github = None
        else:
            try:
                auth = Auth.Token(github_token)
                self.github = Github(auth=auth)
                
                # Test authentication
                user = self.github.get_user()
                print(f"✅ Authenticated as: {user.login}")
                print(f"✅ API Rate Limit: {self.github.get_rate_limit().core.remaining}/5000\n")
            except Exception as e:
                print(f"❌ GitHub authentication failed: {e}")
                self.github = None
    
    def get_language_stats(self, repos) -> Dict[str, float]:
        """Get programming language statistics"""
        language_bytes = Counter()
        
        for repo in repos:
            try:
                languages = repo.get_languages()
                language_bytes.update(languages)
            except Exception:
                continue
        
        total_bytes = sum(language_bytes.values())
        if total_bytes == 0:
            return {}
        
        language_percentages = {
            lang: round((bytes_count / total_bytes) * 100, 2)
            for lang, bytes_count in language_bytes.items()
        }
        
        sorted_languages = sorted(
            language_percentages.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]

        return dict(sorted_languages)
    
    def extract_skills_from_readme(self, repo) -> Set[str]:
        """Extract technologies from README"""
        skills = set()
        
        try:
            readme = repo.get_readme()
            content = readme.decoded_content.decode('utf-8').lower()
            
            for skill in Config.TECH_SKILLS:
                if skill.lower() in content:
                    skills.add(skill)
        except Exception:
            pass
        
        return skills
    
    def analyze_commit_patterns(self, repos) -> Dict[str, Any]:
        """Analyze commit activity"""
        total_commits = 0
        total_stars = 0
        total_forks = 0
        
        for repo in repos:
            try:
                total_commits += repo.get_commits().totalCount
                total_stars += repo.stargazers_count
                total_forks += repo.forks_count
            except Exception:
                continue
        
        return {
            "total_commits": total_commits,
            "total_stars": total_stars,
            "total_forks": total_forks
        }
    
    def analyze_profile(self, username: str) -> Dict[str, Any]:
        """Main function to analyze GitHub profile"""
        print(f"🔍 Analyzing GitHub profile: {username}")
        
        if not self.github:
            print("❌ GitHub API not initialized")
            return {}
        
        try:
            user = self.github.get_user(username)
            repos = list(user.get_repos(type='owner'))
            
            languages = self.get_language_stats(repos)
            
            readme_skills = set()
            for repo in repos[:10]:
                readme_skills.update(self.extract_skills_from_readme(repo))
            
            activity = self.analyze_commit_patterns(repos)
            
            profile = {
                "username": username,
                "name": user.name or username,
                "bio": user.bio or "",
                "location": user.location or "",
                "public_repos": user.public_repos,
                "followers": user.followers,
                "following": user.following,
                "languages": languages,
                "skills_from_repos": list(readme_skills),
                "activity": activity,
                "profile_url": f"https://github.com/{username}",
                "top_repositories": [
                    {
                        "name": repo.name,
                        "description": repo.description,
                        "language": repo.language,
                        "stars": repo.stargazers_count,
                        "url": repo.html_url
                    }
                    for repo in sorted(repos, key=lambda r: r.stargazers_count, reverse=True)[:5]
                ]
            }
            
            print(f"✅ Found {len(languages)} languages")
            print(f"✅ Extracted {len(readme_skills)} skills")
            print(f"✅ Total commits: {activity['total_commits']}\n")
            
            return profile
            
        except GithubException as e:
            print(f"❌ GitHub API Error: {e}")
            return {}
        except Exception as e:
            print(f"❌ Error: {e}")
            return {}
