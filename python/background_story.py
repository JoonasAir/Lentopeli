import textwrap
import shutil


# background story of the game (Y/N) = (player can read or skip the story)

def background_story(screen_name:str):

    longtext = f"""You are an elite Interpol agent, Agent {screen_name}, tasked with capturing a notorious cybercriminal known only by his alias, Shadow. Shadow is a brilliant hacker and mastermind who has been orchestrating a series of devastating cyber-attacks around the world, including infiltrating the very airports that are supposed to be our last line of defense. His latest exploit has crippled major financial systems, causing widespread chaos. But what's worse—he’s also infiltrating the global aviation infrastructure. Shadow has embedded himself within critical airport systems, tampering with flight schedules, security measures, and communication networks. This dangerous game of cat and mouse has escalated to a new level. Not only is Shadow on the run, but he is actively sabotaging the airports that serve as critical hubs for international travel. As an elite agent, your mission is clear: Track down Shadow and stop him before he plunges the world into an even deeper crisis. But with every move you make, Shadow makes another—hiding in plain sight at airports, using his control over the systems to cause mayhem. He is manipulating security checkpoints, redirecting flights, and even triggering false alarms to create diversions, all while staying just a few steps ahead of you. You must race against time, navigating airports where things are never what they seem. The deeper you go, the more you'll realize that Shadow is not just hiding—he’s actively manipulating the environment around you. Can you catch him before the entire global airport network collapses?"""

    terminal_width = shutil.get_terminal_size().columns

    wrapped_text = textwrap.fill(longtext, width = terminal_width-10)

    formatted_text = wrapped_text.replace("\n", "\n\n")
    final_text = formatted_text.replace(".", ". ")

    ask = input("\n\nWould you like to read background story for the game? (Y)es (N)o:")

    if ask.upper() == "Y":
        print(f"\n\n{final_text}")
        input("\n\nPress enter to begin the game.")
    else:
        pass    


if __name__ == "__main__":
    game_dict = {"screen_name": "jorma"}
    background_story(game_dict)
    