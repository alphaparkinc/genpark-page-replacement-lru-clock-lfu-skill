"""Virtual Memory Page Replacement Engine
100% Python Standard Library.
"""

class PageReplacementSimulator:
    """LRU and Second-Chance Clock page frame replacement."""
    def __init__(self, num_frames=3):
        self.num_frames = num_frames

    def lru(self, reference_string):
        frames = []
        page_faults = 0
        for page in reference_string:
            if page in frames:
                frames.remove(page)
                frames.append(page)
            else:
                page_faults += 1
                if len(frames) >= self.num_frames:
                    frames.pop(0)
                frames.append(page)
        return {"page_faults": page_faults, "final_frames": frames}

    def clock(self, reference_string):
        frames = [-1] * self.num_frames
        ref_bits = [0] * self.num_frames
        pointer = 0
        page_faults = 0

        for page in reference_string:
            if page in frames:
                idx = frames.index(page)
                ref_bits[idx] = 1
            else:
                page_faults += 1
                while ref_bits[pointer] == 1:
                    ref_bits[pointer] = 0
                    pointer = (pointer + 1) % self.num_frames
                frames[pointer] = page
                ref_bits[pointer] = 1
                pointer = (pointer + 1) % self.num_frames

        return {"page_faults": page_faults, "final_frames": frames}
