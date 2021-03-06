import os

from Bio import Entrez, SeqIO
from pyensembl_custom import EnsemblRelease

ensembl = EnsemblRelease(release=99, species="danio_rerio")


def get_gene(global_data):
    global_data.logger.log(f"Searching for {global_data.target_sequence}")
    ensembl_gene = None
    try:
        ensembl_gene = ensembl.gene_by_id(gene_id=global_data.target_sequence)
    except ValueError as value_error:
        global_data.logger.log(f"Could not find gene in the ensembl database Error: {value_error}")
        global_data.logger.log(f" Attempting to download danio_rerio information")
        ensembl.download()
        ensembl.index()
        ensembl_gene = ensembl.gene_by_id(gene_id=global_data.target_sequence)

    global_data.logger.log(f"Found {len(ensembl_gene.transcripts)} transcripts for gene {ensembl_gene.gene_name}")
    global_data.ensembl_gene = ensembl_gene

    return global_data


def separate_gene_transcripts(global_data):
    transcripts = {}
    valid_transcripts = []
    for transcript in global_data.ensembl_gene.transcripts:
        transcripts[transcript.transcript_name] = transcript
        valid_transcripts.append(transcript.transcript_name)
    global_data.transcripts = transcripts
    global_data.valid_transcripts = valid_transcripts

    return global_data


def get_promoter_sequence(global_data):
    Entrez.email = "k.patel1098@gmail.com"
    handle = Entrez.efetch(db="nucleotide", id=global_data.input_promoter, rettype="gb", retmode="text")
    record = SeqIO.read(handle, "genbank")
    global_data.promoter = record

    return global_data
