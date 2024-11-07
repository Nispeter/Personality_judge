import time
from flask import Flask, request, jsonify
import argparse
from scienceworld import ScienceWorldEnv

app = Flask(__name__)

env = None
current_observation = None
current_score = 0
is_completed = False
cur_iter = 0

@app.route("/init", methods=["POST"])
def init_environment():
    global env, current_observation, current_score, is_completed, cur_iter

    data = request.json
    task_idx = data.get('task_num', 13)
    simplification_str = data.get('simplification_str', '')
    num_episodes = data.get('num_episodes', 1)
    env_step_limit = data.get('env_step_limit', 100)
    jar_path = data.get('jar_path', '')

    env = ScienceWorldEnv("", jar_path, envStepLimit=env_step_limit)
    task_names = env.get_task_names()
    task_name = task_names[task_idx]
    env.load(task_name, 0, simplification_str)
    current_observation, _ = env.reset()
    current_score = 0
    is_completed = False
    cur_iter = 0

    return next_step(action="look around")

@app.route("/action", methods=["POST"])
def next_action():
    global env, current_observation, current_score, is_completed, cur_iter

    data = request.json
    action = data.get("action")

    if env is None:
        return jsonify({"error": "Environment not initialized. Call /init first."}), 400

    if is_completed:
        return jsonify({"error": "Episode completed. Call /init to start a new episode."}), 400

    observation, reward, is_completed, info = env.step(action)
    current_observation = observation
    current_score = info['score']
    cur_iter += 1

    response = {
        "observation": observation,
        "reward": reward,
        "is_completed": is_completed,
        "score": current_score
    }
    return jsonify(response)

@app.route("/valid_actions", methods=["POST"])
def get_valid_actions():
    if env is None:
        return jsonify({"error": "Environment not initialized. Call /init first."}), 400
    validActions = env.get_valid_action_object_combinations_with_templates()
    action_names = [action['action'] for action in validActions]
    return jsonify({"valid_actions": action_names})


@app.route("/step", methods=["POST"])
def next_step(action=None):
    global env, current_observation, current_score, is_completed, cur_iter

    if env is None:
        return jsonify({"error": "Environment not initialized. Call /init first."}), 400

    if is_completed:
        return jsonify({"error": "Episode completed. Call /init to start a new episode."}), 400

    data = request.json
    if action is None:
        action = data.get("action")

    if not action:
        return jsonify({"error": "No action provided"}), 400

    observation, reward, is_completed, info = env.step(action)
    current_observation = observation
    current_score = info['score']
    cur_iter += 1

    prompt = f"""
    You are controlling an agent in a text-based science simulation game. 
    The current state is as follows:
    Observation: {observation}
    Inventory: {env.inventory()}
    Valid actions: {[action['action'] for action in env.get_valid_action_object_combinations_with_templates()]}

    What should be the next action? Return just the action name without any additional text or punctuation.
    """
    
    response = {
        "prompt": prompt,
        "current_step": cur_iter,
        "reward": reward,
        "is_completed": is_completed,
        "score": current_score
    }
    return jsonify(response)


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
    app.run(host="0.0.0.0", port=5000)