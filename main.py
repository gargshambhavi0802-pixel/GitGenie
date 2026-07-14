from crew.crew import gitgenie_crew

def main():

    print("=" * 60)
    print("        GitGenie Multi-Agent System")
    print("=" * 60)

    result = gitgenie_crew.kickoff()

    print("\n")
    print("=" * 60)
    print("FINAL OUTPUT")
    print("=" * 60)
    print(result)


if __name__ == "__main__":
    main()