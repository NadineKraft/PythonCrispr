class FastaDictionary:

    def lookup(self, chromosome: str):
        raise NotImplementedError

    def size(self, chromosome: str):
        raise NotImplementedError

    def exists(self, chromosome: str):
        raise NotImplementedError


class SimpleFastaDictionary(FastaDictionary):
    dictionary = {
        "chr1": "NC_000001.11",
        "chr2": "NC_000002.12",
        "chr3": "NC_000003.12",
        "chr4": "NC_000004.12",
        "chr5": "NC_000005.10",
        "chr6": "NC_000006.12",
        "chr7": "NC_000007.14",
        "chr8": "NC_000008.11",
        "chr9": "NC_000009.12",
        "chr10": "NC_000010.11",
        "chr11": "NC_000011.10",
        "chr12": "NC_000012.12",
        "chr13": "NC_000013.11",
        "chr14": "NC_000014.9",
        "chr15": "NC_000015.10",
        "chr16": "NC_000016.10",
        "chr17": "NC_000017.11",
        "chr18": "NC_000018.10",
        "chr19": "NC_000019.10",
        "chr20": "NC_000020.11",
        "chr21": "NC_000021.9",
        "chr22": "NC_000022.11",
        "chrX": "NC_000023.11",
        "chrY": "NC_000024.10",
    }

    def exists(self, chromosome: str):
        return self.dictionary.__contains__(chromosome)

    def lookup(self, chromosome: str):
        return self.dictionary.get(chromosome, "invalid chromosome name")

    def size(self, chromosome: str):
        return self.dictionary.get(chromosome)
