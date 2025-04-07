let currentSongIndex = 0;
let songItem = [];

const playerBoxVisibility = document.getElementById('player-box');
const audioPlayer = document.getElementById('audio-player');

const playBtn = document.getElementById('play-btn');
const nextBtn = document.getElementById('next-btn');
const prevBtn = document.getElementById('prev-btn');


const progressBar = document.getElementById('progress-bar');


const nowPlayingTitle = document.getElementById('now-playing-title');
const nowPlayingArtist = document.getElementById('now-playing-artist');

const currentTimeElement = document.getElementById('current-time');
const durationElement = document.getElementById('duration');

const volumeControl = document.getElementById('volume-control');
const muteBtn = document.getElementById('mute-btn');

// Load a song into the player
function loadSong(index) {


    const song = songItem[index];
    const songSrc = song.getAttribute('data-src');
    audioPlayer.src = songSrc;


    audioPlayer.play();
    playBtn.innerHTML = '<i class="fa-solid fa-pause"></i>';

    const songTitle = song.querySelector('#song-title').textContent;
    const songArtist = song.querySelector('#song-artist').textContent;
    nowPlayingTitle.textContent = `${songTitle}`
    nowPlayingArtist.textContent = `${songArtist}`

    
    audioPlayer.addEventListener('loadedmetadata', () => {
        durationElement.textContent = formatTime(audioPlayer.duration);
    });

}

// Format Time
function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${minutes}:${secs < 10 ? '0' : ''}${secs}`;
}

// Play/Pause button

playBtn.addEventListener('click',function(){
    if(audioPlayer.paused){
        audioPlayer.play();
        playBtn.innerHTML = '<i class="fa-solid fa-pause"></i>'
    }
    else{
        audioPlayer.pause();
        playBtn.innerHTML = '<i class="fa-solid fa-play"></i>';
    }
})

// Next button
nextBtn.addEventListener('click',function(){
    currentSongIndex = (currentSongIndex+1)%songItem.length;
    loadSong(currentSongIndex);
})


// Previous button
prevBtn.addEventListener('click',function(){
    currentSongIndex = (currentSongIndex-1+songItem.length)%songItem.length;
    loadSong(currentSongIndex)
})


// Volume Control
volumeControl.addEventListener('input',function(){
    audioPlayer.volume = 
})


// Update progress bar as the song plays
audioPlayer.addEventListener('timeupdate',function(){
    const progressPercent = (audioPlayer.currentTime/audioPlayer.duration)*100;
    progressBar.style.width = `${progressPercent}%`;
    progressBar.setAttribute('aria-valuenow',progressPercent);

    currentTimeElement.textContent = formatTime(audioPlayer.currentTime);

});


// Seek through the song when the progress bar is clicked
const progressContainer = document.querySelector('.progress');
progressContainer.addEventListener('click',function(e){
    const rect = progressContainer.getBoundingClientRect();
    const clickPosition = e.clientX - rect.left;
    const progressPercent = (clickPosition/rect.width)*100;
    const seekTime = (progressPercent/100)*audioPlayer.duration;
    audioPlayer.currentTime = seekTime;
})


// When a page is loaded
document.addEventListener('DOMContentLoaded',function(){

    // To play a song
    songItem = document.querySelectorAll('.song-item');
    
    // To load pagetype
    const pageType = document.body.dataset.pageType;

    // Click on a song to play it
    songItem.forEach((item, index) => {
        item.addEventListener('click', () => {
            // Debugging
            console.log("Song clicked:", index, item.getAttribute('data-src'));

            currentSongIndex = index;
            
            loadSong(currentSongIndex);
            
            playerBoxVisibility.classList.remove("d-none");
            
        });
    });

    // Checks whether pageType is playlist
    if (pageType === 'playlist'){

        const playlistPlayAll = document.getElementById("playlist-play-all");

        // To play the playlist songs
        if (playlistPlayAll){
            playlistPlayAll.addEventListener("click",function(){
                if(songItem.length > 0){
                    currentSongIndex=0;
                    loadSong(currentSongIndex);
                    playerBoxVisibility.classList.remove("d-none");
                }
            });
        }

        // Automatically plays the next song
        audioPlayer.addEventListener('ended',function(){
            console.log("Triggered ended")
            if(songItem.length > 0){
                currentSongIndex = (currentSongIndex + 1) % songItem.length;
                loadSong(currentSongIndex);
            }
        })

    }

})
