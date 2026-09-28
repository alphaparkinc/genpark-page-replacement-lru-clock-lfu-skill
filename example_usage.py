from client import PageReplacementSimulator

def main():
    sim = PageReplacementSimulator(num_frames=3)
    refs = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2]
    res_lru = sim.lru(refs)
    res_clock = sim.clock(refs)
    print("Page Replacement Verification:")
    print(f"LRU Page Faults: {res_lru['page_faults']}")
    print(f"Clock Page Faults: {res_clock['page_faults']}")

if __name__ == "__main__":
    main()
