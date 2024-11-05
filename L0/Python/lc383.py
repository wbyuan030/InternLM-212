class Solution(object):
    def canConstruct(self, ransomNote, magazine):
        """
        :type ransomNote: str
        :type magazine: str
        :rtype: bool
        """
        magazine = list(magazine)
        for item in ransomNote:
            if item in magazine:
                magazine.remove(item)
                continue
            else:
                return False
        return True
        