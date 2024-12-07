// Images and status text for progress
const images = [
    "/1.png", // Starting image (lazy sloth)
    "/2.png", // Climbing up
    "/3.png", // Working hard
    "/4.png", // Mental health break
    "/5.png", // Completion (Crown)
];

const statuses = [
    "Starting out... Feeling lazy!",
    "Making progress... You're all fired up!",
    "Working hard... Keep it up!",
    "Taking a mental health break... Please wait 2 minutes.",
    "All tasks completed! Great job!",
];

const soundEffects = [
    "/sound1.mp3", // For each image change
    "/sound2.mp3",
    "/sound3.mp3",
    "/sound4.mp3",
];

// DOM elements
const progressImage = document.getElementById("progressImage");
const taskButton = document.getElementById("taskButton");
const statusText = document.getElementById("statusText");
let currentIndex = 0;

// Function to play sound
function playSound(index) {
    const audio = new Audio(soundEffects[index]);
    audio.play();
}

// Handle button clicks
taskButton.addEventListener("click", () => {
    if (currentIndex < images.length - 1) {
        currentIndex++;

        // Update image and status
        progressImage.src = images[currentIndex];
        statusText.textContent = statuses[currentIndex];
        playSound(currentIndex);

        // Handle mental health break (disable button for 2 minutes)
        if (currentIndex === 3) {
            taskButton.disabled = true;
            setTimeout(() => {
                taskButton.disabled = false;
            }, 120000); // 2 minutes
        }

        // Update button text for the last step
        if (currentIndex === images.length - 1) {
            taskButton.textContent = "Completed!";
            taskButton.disabled = true; // Disable button on final step
        }
    }
});
