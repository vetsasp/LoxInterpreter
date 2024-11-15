def isPalindrome(s: str) -> bool:
    l, r = 0, len(s) - 1
    curr = lambda i: s[i].lower()

    while l < r:
        while not s[l].isalpha() and l < r:
            l += 1
        while not s[r].isalpha() and r > l:
            r -= 1
        if l >= r:
            break
        if curr(l) != curr(r):
            return False
        l += 1
        r -= 1 
    return True 



def main():
    isPali = lambda x: x == x[::-1]
    
    assert isPalindrome("racecar"), "1"
    assert isPalindrome("Race car?"), "2"
    assert isPalindrome("how about a sentence ecne tneSA TUO Ba././1348 woh"), "3"
    assert not isPalindrome("FRANK"), "4"

    return

if __name__ == "__main__":
    main()