"""Master terminal launcher for 14 weeks, main labs, and assignments."""
from pathlib import Path
import subprocess, sys
ROOT=Path(__file__).resolve().parent
WEEKS_DIR=ROOT/"weeks"
WEEKS=[(1,"Agentic Chatbot"),(2,"Tool Using Agent"),(3,"Skill Creation"),(4,"Memory and Retrieval"),(5,"MCP Style Connector"),(6,"Personal Agent Runtime"),(7,"Agentic Node Graph"),(8,"Parallel Swarm"),(9,"Deep Research Agent"),(10,"Cloud Operations Agent"),(11,"Agentic SDLC Factory"),(12,"Safety Evaluation Governance"),(13,"Discipline Specific Engineering Agents"),(14,"Capstone Project Studio")]
def week_dir(n,t): return WEEKS_DIR/f"Week_{n:02d}_{t.replace(' ','_')}"
def run(path,label):
 if not path.is_file(): print(f"\n[ERROR] Missing file: {path}"); return
 print("\n"+"="*70+f"\nRUNNING {label}\n"+"="*70+"\n",flush=True)
 try:
  result=subprocess.run([sys.executable,str(path)],cwd=str(path.parent),check=False)
  print("\n[COMPLETED]" if result.returncode==0 else f"\n[EXIT CODE {result.returncode}]")
 except KeyboardInterrupt: print("\n[STOPPED] Execution interrupted.")
def question(d,a):
 p=d/f"Assignment_{a}"/"ASSIGNMENT_QUESTION.md"
 print("\n"+"="*70)
 print(p.read_text(encoding="utf-8") if p.exists() else "Assignment question file not found.")
 print("="*70)
def week_menu(n,t):
 d=week_dir(n,t)
 while True:
  print("\n"+"="*70+f"\n WEEK {n}: {t.upper()}\n"+"="*70)
  print("1. Run main lab program\n2. Run Assignment 1\n3. Run Assignment 2\n4. View Assignment 1 question\n5. View Assignment 2 question\n0. Back to week selection")
  c=input("\nChoose an option: ").strip()
  if c=="0": return
  if c=="1": run(d/"main.py",f"Week {n} Main Lab")
  elif c=="2": run(d/"Assignment_1"/"main.py",f"Week {n} Assignment 1")
  elif c=="3": run(d/"Assignment_2"/"main.py",f"Week {n} Assignment 2")
  elif c=="4": question(d,1)
  elif c=="5": question(d,2)
  else: print("Invalid option. Choose 0 to 5.")
  input("\nPress Enter to continue...")
def main():
 while True:
  print("\n"+"="*70+"\n       AGENTIC AI SYSTEMS — MASTER LAB CONSOLE\n"+"="*70)
  for n,t in WEEKS: print(f"{n:02d}. Week {n}: {t}")
  print("\n0. Exit")
  c=input("\nEnter week number (0-14): ").strip()
  if c=="0": print("Goodbye!"); return
  try: n=int(c)
  except ValueError: print("Enter a valid number."); continue
  item=next((x for x in WEEKS if x[0]==n),None)
  if item: week_menu(*item)
  else: print("Choose a week from 1 to 14, or 0 to exit.")
if __name__=="__main__": main()
