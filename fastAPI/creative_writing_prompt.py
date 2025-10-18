from mcp.server.fastmcp import FastMCP
from typing import Annotated
import random
import os


mcp = FastMCP(name="CreativePrompts", stateless_http=True)


@mcp.prompt("generate_story_starter")
def generate_story_starter(
    genre: Annotated[str, "Story genre, e.g., 'Sci-Fi', 'Fantasy', 'Mystery'"],
    main_character_trait: Annotated[str, "A short description of the protagonist (e.g., 'A skeptical detective')"],
    setting: Annotated[str, "Brief setting description (e.g., 'A city where it never stops raining')"],
) -> str:
    """
    Generate the beginning of a creative story based on provided elements.

    Creates the first two paragraphs of a story using the given genre, character, and setting.
    The story will be vivid, immersive, and end with a compelling question or cliffhanger.
    """
    genre_text = (genre or "").strip()
    trait_text = (main_character_trait or "").strip()
    setting_text = (setting or "").strip()

    if not genre_text or not trait_text or not setting_text:
        raise ValueError("genre, main_character_trait, and setting must all be provided")

    # Generate a creative story using intelligent templates and randomization
    story_templates = {
        "horror": [
            "The {trait} stepped into the {setting}, their {sense} immediately detecting something that didn't belong. The air itself seemed to {atmosphere}, and every shadow held a {mystery}.",
            "As they ventured deeper, the {setting} revealed its true nature - {description}. The {trait} realized they weren't alone, and whatever shared this space with them was {threat}."
        ],
        "sci-fi": [
            "The {trait} activated their {tech} as they entered the {setting}, scanning for {scan_target}. The {atmosphere} of the place was unlike anything they'd encountered - {description}.",
            "Their {tech} readings showed {data}, but something was wrong. The {setting} wasn't what it appeared to be, and the {trait} found themselves questioning {reality}."
        ],
        "fantasy": [
            "The {trait} approached the {setting} with {emotion}, sensing the ancient {magic} that permeated every stone. The very air shimmered with {power}, and they could feel {sensation}.",
            "As they crossed the threshold, the {setting} came alive with {activity}. The {trait} realized they had stepped into a world where {discovery}, and now they must {challenge}."
        ],
        "mystery": [
            "The {trait} examined the {setting} with {method}, noting every detail that others might miss. The {evidence} told a story of {incident}, but something didn't add up.",
            "Their {instinct} told them the {setting} held the key to {mystery}, but the deeper they dug, the more questions arose. The {trait} was beginning to suspect {revelation}."
        ]
    }
    
    # Get genre-specific templates or use default
    templates = story_templates.get(genre_text.lower(), story_templates["mystery"])
    
    # Dynamic elements for variety
    elements = {
        "sense": ["instincts", "training", "experience", "intuition"],
        "atmosphere": ["pulse with malevolence", "thicken with anticipation", "crackle with energy", "hum with secrets"],
        "mystery": ["secret", "truth", "answer", "clue"],
        "description": ["beyond comprehension", "defying logic", "impossible yet real", "challenging reality"],
        "threat": ["hungry", "patient", "ancient", "intelligent"],
        "tech": ["scanner", "sensor array", "analysis device", "detection system"],
        "scan_target": ["life signs", "energy readings", "anomalies", "threats"],
        "data": ["impossible readings", "contradictory information", "anomalous patterns", "unexpected results"],
        "reality": ["what was real", "their own perceptions", "the nature of existence", "everything they knew"],
        "emotion": ["caution", "wonder", "determination", "curiosity"],
        "magic": ["power", "energy", "force", "essence"],
        "power": ["potential", "possibility", "mystery", "wonder"],
        "sensation": ["the weight of destiny", "the pull of fate", "the call of adventure", "the whisper of magic"],
        "activity": ["magical phenomena", "otherworldly sights", "impossible events", "fantastical occurrences"],
        "discovery": ["magic was real", "legends were true", "impossible was possible", "dreams could come true"],
        "challenge": ["embrace their destiny", "face their fears", "unlock their potential", "save the world"],
        "method": ["careful observation", "systematic analysis", "deductive reasoning", "logical deduction"],
        "evidence": ["clues", "signs", "traces", "remnants"],
        "incident": ["something terrible", "a great mystery", "an unsolved crime", "a hidden truth"],
        "instinct": ["gut feeling", "professional intuition", "trained senses", "natural ability"],
        "mystery": ["the case", "the truth", "the answer", "the solution"],
        "revelation": ["they were being watched", "nothing was as it seemed", "the truth was stranger than fiction", "they were part of something bigger"]
    }
    
    # Generate story paragraphs
    story_parts = []
    for template in templates:
        # Replace placeholders with random elements
        story_part = template.format(
            trait=trait_text,
            setting=setting_text,
            **{key: random.choice(values) for key, values in elements.items()}
        )
        story_parts.append(story_part)
    
    # Add a compelling cliffhanger
    cliffhangers = [
        f"But as the {trait_text} prepared to leave, they realized the {setting_text} had one final secret to reveal - and it would change everything.",
        f"The {trait_text} knew that what they had discovered in the {setting_text} was only the beginning, and the real challenge lay ahead.",
        f"As they turned to leave the {setting_text}, the {trait_text} couldn't shake the feeling that they were being watched... and that their journey was far from over.",
        f"The {trait_text} left the {setting_text} with more questions than answers, knowing that the truth was still out there, waiting to be discovered."
    ]
    
    story = "\n\n".join(story_parts) + "\n\n" + random.choice(cliffhangers)
    
    return story


if __name__ == "__main__":
    mcp.run(transport="streamable-http")


