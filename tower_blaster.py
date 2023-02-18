import random


def instruction():
    print("Instructions:")
    print(
        "Build a tower by placing the blocks in numerical order progression "
        "from low to the top to high at the bottom of the tower.\n"
        "Finish your tower before your opponent(computer) to win.\n")
    # Explain how Computer works
    print("#Computer Instruction#")
    print("Here are some tips! Let me show you how computer works!.\n"
          "Computer checked the new brick from discard_pile, if larger than 30, "
          "computer would order it from the end of the tower; otherwise!\n"
          "If computer has 6 continuous increasing bricks in the tower.\n"
          "Computer would start find something 'new' from main_piles.\n")
    # Explain Play's rules
    print("#Player Instruction#")
    print("You have bricks from main_pile and discard_pile.\n"
          "The top of is discard_piles is face up! "
          "You could use it, or find something new from main_piles(face_down).\n"
          "You could use top of main_piles, or ignore it and skip this turn!.\n"
          "You may see 'help' bottom in the game. There is no one could help you lol! Enjoy!")
    print(" ")


def setup_bricks():
    main_pile = []
    discard_pile = []
    for i in range(1, 61):
        main_pile.append(i)
    return main_pile, discard_pile  # return a tuple of two lists, main_pile and discard_pile


def shuffle_bricks(bricks):
    random.shuffle(bricks)


def check_bricks(main_pile, discard_pile):
    if len(main_pile) == 0:  # run out of main_pile
        shuffle_bricks(discard_pile)  # shuffle discard_pile
        for i in discard_pile:  # copy from discard_pile and form a main_pile
            main_pile.append(i)
        discard_pile.clear()  # clear discard_pile
        discard_pile.append(get_top_brick(main_pile))  # get the top of main_pile and put it to the discard_pile


def check_tower_blaster(tower):
    tower_sorted = sorted(tower)
    if tower_sorted == tower:  # if tower is sorted with ascending order. #Game is over.
        return True
    else:
        return False


def get_top_brick(brick_pile):
    return brick_pile.pop(0)


def deal_initial_bricks(main_pile):
    com_list = []
    user_list = []
    n = 10  # length of a tower
    while n > 0:
        # get the top of main_pile and assign it to com_list and user_list.
        # #Each new_inserted brick must be the top of the others
        com_list.insert(0, get_top_brick(main_pile))
        user_list.insert(0, get_top_brick(main_pile))
        n -= 1
    return com_list, user_list  # return a tuple of two lists, com_list and user_list


def add_brick_to_discard(brick, discard_pile):
    discard_pile.insert(0, brick)


def find_and_replace(new_brick, brick_to_be_replaced, tower, discard_pile):
    # USER ONLY
    if brick_to_be_replaced in tower:
        add_brick_to_discard(brick_to_be_replaced, discard_pile)  # replaced brick go to discard pile
        brick_to_be_replaced_index = tower.index(brick_to_be_replaced)  # find the index of replaced brick
        tower[brick_to_be_replaced_index] = new_brick  # replaced with new_brick
        return True
    else:  # if replaced_brick not in the tower.
        return False


def long_increasing_subseq(lst):  # find the longest continuous increasing subsequence
    curr_length = next_starting_point = 0
    for i in range(len(lst)):
        if lst[i - 1] >= lst[i]:  # previous > current, stopping point!
            next_starting_point = i  # next possible increasing sub-squ happened at index = i
        curr_length = max(curr_length,
                          i - next_starting_point + 1)  # if not meet stopping point, count length of each sub-seq.
    return curr_length


def computer_play(tower, main_pile, discard_pile):
    print(" ")
    print("COMPUTER's TURN!")
    # computer determine go to discard_pile or main_pile
    # if computer has >6 continuous increasing substring, computer is about to win.
    # And computer may think the "missing/key" bricks are not in the discard_pile, but main_piles.
    # Computer would go to main_piles for more chance
    if long_increasing_subseq(tower) < 6:
        new_brick = get_top_brick(discard_pile)  # take one brick from discard_pile
        print("The computer picked {} from the discard pile.".format(new_brick))
        if new_brick < min(
                tower):  # if new_brick is smaller than all bricks in the tower, we would take it and put it the to top.
            add_brick_to_discard(tower[0],
                                 discard_pile)  # get the top of the tower, and insert it back the top of discard_pile
            tower[0] = new_brick  # top of the tower = new brick
        elif new_brick > max(tower):  # otherwise, put the largest one to the bottom of the tower
            add_brick_to_discard(tower[-1], discard_pile)  # put the bottom of tower to the top of discard_pile
            tower[-1] = new_brick  # put the new_brick to the bottom of tower
        else:  # if new_brick is between top and bottom bricks, we can select a place to locate
            if new_brick < 30:  # if smaller than 30, computer select a suitable place from the top
                i = 0
                while i < 5:  # looping from the beginning to the mid of tower
                    if tower[i] < new_brick < tower[i + 1]:
                        # if new_brick>current and new_brick<next. Replace next with new_brick.
                        # make the sequence more smooth(the difference between bricks are smaller)
                        add_brick_to_discard(tower[i + 1], discard_pile)  # Add next to the discard
                        tower[i + 1] = new_brick  # Make next == new_brick.
                        break
                    i += 1
                else:
                    # can't find a good place from index(0-5), which means new_brick is small and top bricks are large.
                    # put new_brick to the top
                    add_brick_to_discard(tower[0], discard_pile)
                    tower[0] = new_brick
            elif new_brick >= 30:  # larger than 30, computer start searching good place from the bottom.
                j = len(tower) - 1  # from the bottom of the tower
                while j > 3:  # from 9, 8, 7, ....6, 5,4(mid of the tower)
                    if tower[j] > new_brick > tower[j - 1]:  # similar ideas as mentioned
                        add_brick_to_discard(tower[j - 1], discard_pile)
                        tower[j - 1] = new_brick
                        break
                    j -= 1
                else:
                    add_brick_to_discard(tower[-1], discard_pile)
                    tower[-1] = new_brick
    else:
        # Computer take from main_pile
        new_brick = get_top_brick(main_pile)
        print("The computer picked a {} from main_pile! It is about to win!!".format(new_brick))  # a kindly reminder!
        for i in range(0,
                       len(tower) - 1):
            # similar ideas as mentioned,
            # #computer check one by one and find good place to replace bricks.
            if tower[i] < new_brick < tower[i + 1]:
                add_brick_to_discard(tower[i + 1], discard_pile)
                tower[i + 1] = new_brick
                break
            elif new_brick > max(tower):  # if new_brick is larger than all, put it to the end ... (for edge case)
                add_brick_to_discard(tower[-1], discard_pile)
                tower[-1] = new_brick
                break
            elif new_brick < min(tower):
                add_brick_to_discard(tower[0], discard_pile)
                tower[0] = new_brick
                break


def user_play(tower, main_pile, discard_pile):
    # greetings and info.
    print(" ")
    print("NOW IT'S YOUR TIME!")
    print("Your Tower:", tower)
    print("The top brick on the discard_pile is:", discard_pile[0])

    ask_next_step = input("Type 'D' to take the discard brick, 'M' for a mystery brick, or 'H' for help!\n")
    if ask_next_step == "M" or ask_next_step == 'm':
        new_brick = get_top_brick(main_pile)
        print("You picked {} from main pile".format(new_brick))
        ask_take = input("Do you want to use this brick? Type 'Y' or 'N' to skip this turn\n")
        if ask_take.startswith('Y') or ask_take.startswith('y'):
            brick_to_be_replaced = int(
                input("Where do you want to place this brick? Type a brick number in your tower!\n"))
            if find_and_replace(new_brick, brick_to_be_replaced, tower,
                                discard_pile):  # Yes, found it and replace it.
                print("You replaced {} with {} .".format(brick_to_be_replaced, new_brick))
                print("Your Tower:", tower)
            else:
                add_brick_to_discard(new_brick, discard_pile)  # Put the new_brick to the discard_pile.
                print("You enter an invalid number! There is no chance to replace!")
        else:
            discard_pile.insert(0, new_brick)
            print("You don't wanna do replacement. Skip this turn!")
    elif ask_next_step == "D" or ask_next_step == 'd':
        new_brick = get_top_brick(discard_pile)  # get the top of discard_pile as new_brick
        brick_to_be_replaced = int(input(
            "Where do you want to place this brick? Type a brick number in your tower!\n"))  # which one to be replaced?
        if find_and_replace(new_brick, brick_to_be_replaced, tower,
                            discard_pile):  # Yes, found it and replace it.
            print("You replaced {} with {} .".format(brick_to_be_replaced, new_brick))
            print("Your Tower:", tower)
        else:
            add_brick_to_discard(new_brick, discard_pile)  # Put the new_brick to the discard_pile.
            print("You enter an invalid number! There is no chance to replace!")

    else:  # press H for help....
        print("There is no help for implement! Please not select H next time!")


def main():
    instruction()
    game_playing = True
    while game_playing:
        input("Press Enter to start the game\n")
        # setup bricks, shuffle bricks, user and com get ®the bricks
        main_pile, discard_pile = setup_bricks()
        shuffle_bricks(main_pile)
        com_list, user_list = deal_initial_bricks(main_pile)
        discard_pile.insert(0, get_top_brick(main_pile))  # get one card from main_pile to discord
        print('Computer\'s tower:', com_list)
        print('Your Tower:', user_list)


        game_over = False

        while not game_over:
            check_bricks(main_pile, discard_pile)  # check if main_pile is empty
            computer_play(com_list, main_pile, discard_pile)  # computer goes first
            if check_tower_blaster(com_list):  # check if computer won
                print('Computer\'s tower:', com_list)
                print('Computer Won!')
                break
            check_bricks(main_pile, discard_pile)  # check if main_pile is empty
            user_play(user_list, main_pile, discard_pile)
            if check_tower_blaster(user_list):  # check if player won
                game_over = True
                print('Player Won!')
        replay = input("Want to play again? (y/n)\n")
        if replay.startswith('Y') or replay.startswith('y'):
            game_playing = True
        else:
            game_playing = False
    print('Nice job and Good bye!')


if __name__ == "__main__":
    main()
