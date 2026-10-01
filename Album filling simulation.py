import random

# A function that creates a sticker album,
# fills it, and counts how many stickers you had to buy separately
def amount_to_fill(size):
    album=[0]*size
    counter=0
    
    while sum(album)<size:
        sticker=random.randint(0,size-1)
        album[sticker]=1
        counter=counter+1
    
    return counter

# Same as before, but reapeated a certain amount of times
def multi_amount_to_fill(total_stickers, nr_albums):
    step=0
    amounts=[0]*nr_albums

    while step<nr_albums:
        amounts[step]=amount_to_fill(total_stickers)
        step=step+1
        
    return amounts

# Does the average of all the amount of stickers that took to fill multiple albums
def average_stickers(total_stickers, nr_albums):
    average=sum(multi_amount_to_fill(total_stickers, nr_albums))/nr_albums
    
    return average

# Tries different album sizes in a range
# to determine the average amount of stickers that it takes to fill every size
def try_every_size(stickers_min, stickers_max, repeats):
    albums = stickers_max-stickers_min
    amounts = [0]*albums
    stickers = stickers_min
    step=0
    while step<albums:
        amounts[step]=average_stickers(stickers,repeats)
        step=step+1
        stickers= stickers+1
        
    return amounts
    

