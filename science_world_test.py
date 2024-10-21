import time
from openai import OpenAI

client = OpenAI(api_key='')
import argparse
from scienceworld import ScienceWorldEnv

# Set your OpenAI API key here

def ask_gpt(prompt):

    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": prompt}
    ])
    return completion.choices[0].message.content.strip()

 
def chatgptModel(args):
    """ ChatGPT-powered agent for ScienceWorld. """
    exitCommands = ["quit", "exit"]

    taskIdx = args['task_num']
    simplificationStr = args['simplification_str']
    numEpisodes = args['num_episodes']

    finalScores = []
    env = ScienceWorldEnv("", args['jar_path'], envStepLimit=args['env_step_limit'])

    taskNames = env.get_task_names()
    print("Task Names: " + str(taskNames))

    taskName = taskNames[taskIdx]
    env.load(taskName, 0, "")
    maxVariations = env.get_max_variations(taskName)
    print("Starting Task " + str(taskIdx) + ": " + taskName)
    time.sleep(2)

    for episodeIdx in range(0, numEpisodes):
        randVariationIdx = env.get_random_variation_train()
        env.load(taskName, randVariationIdx, simplificationStr)

        initialObs, initialDict = env.reset()
        print("Initial Observation: " + initialObs)

        score = 0.0
        isCompleted = False
        curIter = 0

        userInputStr = "look around"
        while (userInputStr not in exitCommands) and (isCompleted is False):
            print("----------------------------------------------------------------")
            print("Step: " + str(curIter))

            # Send user input, get response from the environment
            observation, reward, isCompleted, info = env.step(userInputStr)
            score = info['score']

            print("\n>>> " + observation)
            print("Reward: " + str(reward))
            print("Score: " + str(score))
            print("isCompleted: " + str(isCompleted))

            if isCompleted:
                break

            # Get valid actions
            validActions = env.get_valid_action_object_combinations_with_templates()

            # Create a prompt for GPT based on current state and valid actions
            prompt = f"""
            You are controlling an agent in a text-based science simulation game. 
            The current state is as follows:
            Observation: {observation}
            Inventory: {env.inventory()}
            Valid actions: {[action['action'] for action in validActions]}

            What should be the next action? Return just the action name without any additional text or punctuation.
            """

            # Ask ChatGPT for the next action
            gptAction = ask_gpt(prompt)
            print(f"ChatGPT suggests: {gptAction}")
            userInputStr = gptAction.lower().strip()

            curIter += 1

        print("Goal Progress:")
        print(env.get_goal_progress_str())
        time.sleep(1)

        finalScores.append(score)
        filenameOutPrefix = args['output_path_prefix'] + str(taskIdx)
        env.store_run_history(episodeIdx, notes={'text': 'my notes here'})
        env.save_run_histories_buffer_if_full(filenameOutPrefix, max_per_file=args['max_episode_per_file'])

    env.save_run_histories_buffer_if_full(filenameOutPrefix, max_per_file=args['max_episode_per_file'], force_save=True)
    avg = sum([x for x in finalScores if x >= 0]) / len(finalScores)
    print(f"\nAverage episode score: {avg}\n")

    print("Completed.")


def build_simplification_str(args):
    simplifications = list()
    if args["teleport"]:
        simplifications.append("teleportAction")
    if args["self_watering_plants"]:
        simplifications.append("selfWateringFlowerPots")
    if args["open_containers"]:
        simplifications.append("openContainers")
    if args["open_doors"]:
        simplifications.append("openDoors")
    if args["no_electrical"]:
        simplifications.append("noElectricalAction")

    return args["simplifications_preset"] or ",".join(simplifications)


def parse_args():
    parser = argparse.ArgumentParser("Run ChatGPT agent in ScienceWorld.")
    parser.add_argument("--jar_path", type=str, help="Path to the ScienceWorld jar file.")
    parser.add_argument("--task-num", type=int, default=13, help="Specify the task number to play.")
    parser.add_argument("--var-num", type=int, default=0, help="Specify the task variation.")
    parser.add_argument("--env-step-limit", type=int, default=100, help="Step limit for the environment.")
    parser.add_argument("--num-episodes", type=int, default=5, help="Number of episodes to run.")
    parser.add_argument("--output_path_prefix", type=str, default="./output/", help="Path prefix for output files.")
    parser.add_argument("--max_episode_per_file", type=int, default=10, help="Max episodes per output file.")
    parser.add_argument("--simplifications_preset", type=str, default=None, help="Simplifications preset.")
    parser.add_argument("--teleport", action='store_true', help="Enable teleport simplification.")
    parser.add_argument("--self_watering_plants", action='store_true', help="Enable self-watering plants.")
    parser.add_argument("--open_containers", action='store_true', help="Enable auto-open containers.")
    parser.add_argument("--open_doors", action='store_true', help="Enable auto-open doors.")
    parser.add_argument("--no_electrical", action='store_true', help="Disable electrical actions.")

    return vars(parser.parse_args())


if __name__ == "__main__":
    args = parse_args()
    args['simplification_str'] = build_simplification_str(args)
    chatgptModel(args)
